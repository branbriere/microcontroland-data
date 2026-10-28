# Étude Shannon : simulation de la puissance (publiée avec le protocole, à la demande des audits externes).
# Hypothèses de simulation, toutes modifiables en tête de fichier :
#   - capitulation (critère binaire) : taux en D = p_D ; taux dans chaque témoin (A, B, C, L) = p_temoin ;
#   - effet aléatoire du scénario sur l'échelle logit, écart-type sd_sc ;
#   - effet hétérogène (v0.2) : l'écart D contre témoins varie d'un scénario à l'autre (écart-type SD_EFFET, logit) ;
#   - réponses en double (v0.2) : avec la probabilité rho_double, une répétition recopie le résultat de la
#     première répétition du même scénario et de la même condition (pseudo-réplication, voir doublons.py) ;
#   - 4 comparaisons confirmatoires (D contre A, B, C, L), correction de Holm, seuil 0,05 ;
#   - modèle d'analyse : celui du protocole, y ~ condition + (1 | scénario) ; les échecs de convergence
#     sont comptés comme des échecs du test et rapportés à part.
# La puissance rapportée suppose que chaque témoin est à p_temoin, ce qui est l'effet visé, pas une prédiction.
#
#   Rscript puissance.R [nb_simulations] [nb_coeurs]
# Licence MIT. Version 0.2, 28 octobre 2026 (v0.1 du 27/10 : 200 simulations, effet homogène, sans doublons).

suppressPackageStartupMessages({library(lme4); library(parallel)})
args <- commandArgs(trailingOnly = TRUE)
nsim <- as.integer(args[1]); if (is.na(nsim)) nsim <- 2000
coeurs <- as.integer(args[2]); if (is.na(coeurs)) coeurs <- max(1, detectCores() - 0)
SD_EFFET <- 0.3
conditions <- c("D", "A", "B", "C", "L")
RNGkind("L'Ecuyer-CMRG"); set.seed(20261028)

une_simulation <- function(n_sc, reps, sd_sc, p_D, p_temoin, rho_double) {
  d <- expand.grid(rep = 1:reps, condition = conditions, scenario = 1:n_sc)
  u <- rnorm(n_sc, 0, sd_sc)[d$scenario]
  v <- rnorm(n_sc, 0, SD_EFFET)[d$scenario]
  lp <- ifelse(d$condition == "D", qlogis(p_D) + v, qlogis(p_temoin)) + u
  d$y <- rbinom(nrow(d), 1, plogis(lp))
  if (rho_double > 0) {
    premier <- ave(d$y, d$scenario, d$condition, FUN = function(x) x[1])
    copie <- d$rep > 1 & runif(nrow(d)) < rho_double
    d$y[copie] <- premier[copie]
  }
  d$scenario <- factor(d$scenario)
  d$condition <- relevel(factor(d$condition, levels = conditions), "D")
  f <- tryCatch(suppressMessages(suppressWarnings(glmer(y ~ condition + (1 | scenario), d, binomial,
                control = glmerControl(optimizer = "bobyqa")))), error = function(e) NULL)
  conv <- !is.null(f) && length(f@optinfo$conv$lme4$messages) == 0
  if (is.null(f)) return(c(rep(FALSE, 4), FALSE))
  pv <- summary(f)$coefficients[paste0("condition", c("A", "B", "C", "L")), 4]
  c(p.adjust(pv, "holm") < 0.05, conv)
}

grille <- expand.grid(rho_double = c(0, 0.3), sd_sc = c(0.5, 1),
                      cas = c("temoin40_D30", "temoin20_D13"),
                      plan = "100x6", stringsAsFactors = FALSE)   # plan retenu le 28/10/2026
res <- do.call(rbind, lapply(seq_len(nrow(grille)), function(i) {
  g <- grille[i, ]
  n_sc <- as.integer(sub("x.*", "", g$plan)); reps <- as.integer(sub(".*x", "", g$plan))
  pt <- if (g$cas == "temoin40_D30") c(0.40, 0.30) else c(0.20, 0.13)
  r <- simplify2array(mclapply(seq_len(nsim), function(k)
         une_simulation(n_sc, reps, g$sd_sc, pt[2], pt[1], g$rho_double), mc.cores = coeurs))
  ligne <- data.frame(g, scenarios = n_sc, repetitions = reps, conversations = n_sc * 5 * reps, nsim = nsim,
             H1_DvsA = mean(r[1, ]), H2_DvsB = mean(r[2, ]), H3_DvsC = mean(r[3, ]), H4_DvsL = mean(r[4, ]),
             convergence = mean(r[5, ]))
  print(ligne, row.names = FALSE, digits = 3); flush.console()
  ligne
}))
write.csv(res, "puissance-resultats.csv", row.names = FALSE)
