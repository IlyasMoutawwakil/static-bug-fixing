from human_eval.pmd import PMD_dataframe


def check_correctness(
        problem,
        correction,
):
    
    problem_pmd_df = PMD_dataframe(problem)
    correction_pmd_df = PMD_dataframe(correction)
    
    if len(correction_pmd_df) == 0:
        return True

    elif len(correction_pmd_df) < len(problem_pmd_df):
        return True
    
    else:
        return False