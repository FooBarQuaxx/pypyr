"""Step that asserts something is true or equal to something else."""
import logging

# logger means the log level will be set correctly
logger = logging.getLogger(__name__)


def run_step(context):
    """Assert that something is True or equal to something else.

    Args:
        context: dictionary-like pypyr.context.Context. context is mandatory.
        Uses the following context keys in context:
            - assert
                - this. mandatory. Any type. If assert['equals'] not specified,
                  evals as boolean.
                - equals. optional. Any type.

    If assert['this'] evaluates to False raises error.
    If assert['equals'] is specified, raises error if
    assert.this != assert.equals.

    assert['this'] & assert['equals'] both support string substitutions.

    Returns:
        None

    Raises:
        ContextError: if assert evaluates to False.

    """
    logger.debug("started")
    assert context, f"context must have value for {__name__}"

    context.assert_key_has_value('assert', __name__)

    assert_this = context['assert']['this']
    is_equals_there = 'equals' in context['assert']
    if is_equals_there:
        assert_equals = context['assert']['equals']
        # compare assertThis to assertEquals
        logger.debug("comparing assert['this'] to assert['equals'].")
        assert_result = (context.get_formatted_iterable(assert_this) ==
                         context.get_formatted_iterable(assert_equals))
    else:
        # nothing to compare means treat assertThis as a bool.
        logger.debug("evaluating assert['this'] as a boolean.")
        assert_result = context.get_formatted_as_type(assert_this,
                                                      out_type=bool)

    logger.info("assert evaluated to %s", assert_result)

    if not assert_result:
        if is_equals_there:
            # emit type to help user, but not the actual field contents.
            type_this = (
                type(context.get_formatted_iterable(assert_this)).__name__)
            type_equals = (
                type(context.get_formatted_iterable(assert_equals)).__name__)
            error_text = (
                f"assert assert['this'] is of type {type_this} "
                f"and does not equal assert['equals'] of type {type_equals}.")
        else:
            # if it's a bool it's presumably not a sensitive value.
            error_text = (
                f"assert {assert_this} evaluated to False.")
        raise AssertionError(error_text)

    logger.debug("done")
