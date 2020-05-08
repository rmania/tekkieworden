import logging
import pandas as pd


def pandas_join_key_single(left_df, right_df, key, how):

    """
    perform left join with single key (identical key)
    """

    logging.info(f"left_df shape: {left_df.shape}")
    logging.info(f"right_df shape: {right_df.shape}")

    logging.info(f"joining on key: {key}")

    joined_df = left_df.merge(right_df, how=how, on=key, indicator=True)

    logging.info(f"Join result\n{joined_df._merge.value_counts()}")
    # joined_df = joined_df.drop("_merge", axis=1)

    logging.info(f"joined df: {joined_df.shape}")

    return joined_df


def pandas_join_key_dual(left_df, right_df, left_key, right_key, how):

    """
    perform join with dual keys (multiple)
    """

    logging.info(f"left_df shape: {left_df.shape}")
    logging.info(f"right_df shape: {right_df.shape}")

    logging.info(f"joining on left_key: {left_key}")
    logging.info(f"joining on right_key: {right_key}")

    joined_df = left_df.merge(
        right_df, how=how, left_on=left_key, right_on=right_key, indicator=True
    )
    # validate='one_to_many')

    logging.info(f"Join result\n{joined_df._merge.value_counts()}")
    # joined_df = joined_df.drop("_merge", axis=1)

    logging.info(f"joined df: {joined_df.shape}")

    return joined_df


def pandas_join_on_index(left_df, right_df, how="inner"):
    """
    Perform join on identical indices.
    Args:
        left_df:
        right_df:
        how:
    Returns:
    """

    logging.info(f"left_df shape: {left_df.shape}")
    logging.info(f"right_df shape: {right_df.shape}")

    logging.info(f"joining on left_indices: {[i for i in left_df.index.names]}")
    logging.info(f"joining on left_key: {[i for i in right_df.index.names]}")

    joined_df = pd.merge(
        left_df, right_df, how=how, left_index=True, right_index=True, indicator=True
    )

    logging.info(f"Join result\n\t{joined_df._merge.value_counts()}")
    joined_df = joined_df.drop("_merge", axis=1)

    logging.info(f"joined df: {joined_df.shape}")

    return joined_df
