"""
Disagreement measures for the Committee model.
"""

import numpy as np
from collections import Counter
from scipy.stats import entropy


def vote_entropy(committee, X, **predict_proba_kwargs):
    """
    Calculates the vote entropy for the Committee. First it computes the
    predictions of X for each learner in the Committee, then calculates
    the probability distribution of the votes. The entropy of this distribution
    is the vote entropy of the Committee, which is returned.

    Parameters
    ----------
    committee: modAL.models.Committee object
        The Committee instance for which the vote entropy is to be calculated.

    X: numpy.ndarray of shape (n_samples, n_features)
        The data for which the vote entropy is to be calculated.

    predict_proba_kwargs: keyword arguments
        Keyword arguments for the predict_proba method of the Committee.

    Returns
    -------
    entr: numpy.ndarray of shape (n_samples, )
        Vote entropy of the Committee for the samples in X.
    """
    n_learners = len(committee)
    votes = committee.vote(X, **predict_proba_kwargs)
    vote_proba = np.zeros(shape=(X.shape[0], len(committee.classes_)))
    entr = np.zeros(shape=(X.shape[0],))

    for vote_idx, vote in enumerate(votes):
        vote_counter = Counter(vote)

        for class_idx, class_label in enumerate(committee.classes_):
            vote_proba[vote_idx, class_idx] = vote_counter[class_label]/n_learners

        entr[vote_idx] = entropy(vote_proba[vote_idx])

    return entr


def vote_uncertainty_entropy(committee, X, **predict_proba_kwargs):
    proba = committee.predict_proba(X)
    entr = np.transpose(entropy(np.transpose(proba)))
    return entr
