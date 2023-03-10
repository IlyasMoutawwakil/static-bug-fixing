import numpy as np


def estimate_pass_at_k(
        num_samples,
        num_correct,
        k
):

    if num_samples - num_correct < k:
        return 1.0
    
    return 1.0 - np.prod(1.0 - k / np.arange(num_samples - num_correct + 1, num_samples + 1))
