import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import joblib
from dotenv import load_dotenv
from sklearn.metrics import classification_report, balanced_accuracy_score
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import wandb

load_dotenv()

#### Import the data
df = pd.read_csv("../data/text_dataset_translate.csv")
Y = df["diag"].values

# Remove CFTD and unclear diagnosis
df["diag"].value_counts()
# Drop the rows with unclear diagnosis
df = df[df["diag"] != "UNCLEAR"]
# Do the same for the X array based on the df index

cv_fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
df["diag"].value_counts()


LANGUAGE = ["fr", "en"]
EMBEDDING_MODEL = ["instructor", "openai"]

Y = df["diag"].values

for lang in LANGUAGE:
    for embedding_method in EMBEDDING_MODEL:
        X = np.load(f"../data/embeddings/{embedding_method}_{lang}_embeddings.npy")

        #########################################
        # MLPC
        param_grid = {
            "hidden_layer_sizes": [(400,), (200,), (100, 100), (200, 200)],
            "activation": ["tanh", "relu"],
            "solver": ["adam"],
            "learning_rate_init": [0.001, 0.01],
            "max_iter": [800, 1500, 2500],
        }

        # Create grid search
        cls = MLPClassifier(random_state=42)
        gs_mlpc = GridSearchCV(
            cls, param_grid, scoring="accuracy", cv=cv_fold, verbose=1
        )
        gs_mlpc.fit(X, Y)
        best_mlpc = gs_mlpc.best_estimator_
        df_cv_search_rf = pd.DataFrame(gs_mlpc.cv_results_)
        # Print the best parameters and score
        print("Best parameters:", gs_mlpc.best_params_)
        print("Best score:", gs_mlpc.best_score_)
        joblib.dump(
            gs_mlpc, f"../models/{embedding_method}_{lang}_gridsearch_mlpc.joblib"
        )
        joblib.dump(best_mlpc, f"../models/{embedding_method}_{lang}_model_mlpc.joblib")

        gs_mlpc = joblib.load(
            f"../models/{embedding_method}_{lang}_gridsearch_mlpc.joblib"
        )
        best_mlpc = joblib.load(
            f"../models/{embedding_method}_{lang}_model_mlpc.joblib"
        )

        # Use cross_val_predict to get predicted labels and probabilities
        y_pred = cross_val_predict(best_mlpc, X, Y, cv=cv_fold)
        y_probas = cross_val_predict(
            best_mlpc, X, Y, cv=cv_fold, method="predict_proba"
        )
        # Compute classification report
        report = classification_report(
            Y, y_pred, target_names=best_mlpc.classes_, output_dict=True
        )

        run = wandb.init(
            project="myo-text-classify",
            name=f"{embedding_method}_{lang}_mlpc",
            config={
                "embedding": f"{embedding_method}",
                "doc_lang": f"{lang}",
                "corpus": "complete_1704023_190reports",
                "model": "MLPClassifier",
            },
        )
        config = wandb.config
        best_params = gs_mlpc.best_params_
        best_score = gs_mlpc.best_score_
        best_std = gs_mlpc.cv_results_["std_test_score"][gs_mlpc.best_index_]
        balanced_accuracy_metric = balanced_accuracy_score(Y, y_pred)

        wandb.log(
            {
                "Classification Report": report,
                "Best Params": best_params,
                "Best Score (gs)": best_score,
                "CV Std Devs (gs)": best_std,
                "Balanced Accuracy": balanced_accuracy_metric,
            }
        )
        wandb.sklearn.plot_confusion_matrix(Y, y_pred, best_mlpc.classes_)
        wandb.sklearn.plot_classifier(
            best_mlpc,
            X,
            X,
            Y,
            Y,
            y_pred,
            y_probas,
            labels=best_mlpc.classes_,
            model_name=f"{embedding_method}_{lang}_model",
            feature_names=None,
        )
        # Create artifact for best model
        model_artifact = wandb.Artifact(
            f"{embedding_method}_{lang}_model_mlpc", type="model"
        )
        # Add best estimator to artifact
        model_artifact.add_file(
            f"../models/{embedding_method}_{lang}_model_mlpc.joblib"
        )
        # Log artifact to WandB
        wandb.run.log_artifact(model_artifact)
        wandb.finish()

        #############################################
        # RANDOM FOREST
        param_grid_rf = {
            "n_estimators": [10, 50, 100, 200],
            "max_depth": [None, 5, 10, 20],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "class_weight": ["balanced", "balanced_subsample"],
        }

        # Create grid search
        cls_rf = RandomForestClassifier(random_state=42)
        gs_rf = GridSearchCV(
            cls_rf, param_grid_rf, scoring="accuracy", cv=cv_fold, verbose=1
        )
        gs_rf.fit(X, Y)
        best_rf = gs_rf.best_estimator_
        df_cv_search_rf = pd.DataFrame(gs_rf.cv_results_)
        # Print the best parameters and score
        print("Best parameters:", gs_rf.best_params_)
        print("Best score:", gs_rf.best_score_)
        joblib.dump(gs_rf, f"../models/{embedding_method}_{lang}_gridsearch_rf.joblib")
        joblib.dump(best_rf, f"../models/{embedding_method}_{lang}_model_rf.joblib")

        gs_rf = joblib.load(f"../models/{embedding_method}_{lang}_gridsearch_rf.joblib")
        best_rf = joblib.load(f"../models/{embedding_method}_{lang}_model_rf.joblib")

        # Use cross_val_predict to get predicted labels and probabilities
        y_pred = cross_val_predict(best_rf, X, Y, cv=cv_fold)
        y_probas = cross_val_predict(best_rf, X, Y, cv=cv_fold, method="predict_proba")
        # Compute classification report
        report = classification_report(
            Y, y_pred, target_names=best_rf.classes_, output_dict=True
        )

        run = wandb.init(
            project="myo-text-classify",
            name=f"{embedding_method}_{lang}_rf",
            config={
                "embedding": f"{embedding_method}",
                "doc_lang": f"{lang}",
                "corpus": "complete_1704023_190reports",
                "model": "RandomForest",
            },
        )
        config = wandb.config
        best_params = gs_mlpc.best_params_
        best_score = gs_mlpc.best_score_
        best_std = gs_mlpc.cv_results_["std_test_score"][gs_mlpc.best_index_]
        balanced_accuracy_metric = balanced_accuracy_score(Y, y_pred)

        wandb.log(
            {
                "Classification Report": report,
                "Best Params": best_params,
                "Best Score (gs)": best_score,
                "CV Std Devs (gs)": best_std,
                "Balanced Accuracy": balanced_accuracy_metric,
            }
        )
        wandb.sklearn.plot_confusion_matrix(Y, y_pred, best_rf.classes_)
        wandb.sklearn.plot_classifier(
            best_rf,
            X,
            X,
            Y,
            Y,
            y_pred,
            y_probas,
            labels=best_rf.classes_,
            model_name=f"{embedding_method}_{lang}_model",
            feature_names=None,
        )
        # Create artifact for best model
        model_artifact = wandb.Artifact(
            f"{embedding_method}_{lang}_model_rf", type="model"
        )
        # Add best estimator to artifact
        model_artifact.add_file(f"../models/{embedding_method}_{lang}_model_rf.joblib")
        # Log artifact to WandB
        wandb.run.log_artifact(model_artifact)
        wandb.finish()
