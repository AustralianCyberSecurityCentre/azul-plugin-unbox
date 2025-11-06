import unittest

from azul_runner import JobResult, State, test_template

from azul_plugin_unbox.main import AzulPluginUnbox


class BaseUnboxPluginTest(test_template.TestPlugin):
    PLUGIN_TO_TEST = AzulPluginUnbox
    unbox_result_key: str
    unbox_type_key: str

    @classmethod
    def setUpClass(cls) -> None:
        """Unittest method."""
        if cls is BaseUnboxPluginTest:
            raise unittest.SkipTest("Template class for plugin tests cannot be run directly")
        super().setUpClass()

    def setUp(self) -> None:
        """Unittest method."""
        # Tried to do this with just a setUpClass method, but for some reason unittest doesn't seem to run
        #  setUpClass when the class is imported to another file but still tries to run the tests.
        if self.__class__ is BaseUnboxPluginTest:
            raise unittest.SkipTest("Template class for plugin tests cannot be run directly")

        super().setUp()

    def get_result_from_cart(self, loaded_cart: bytes, *, format_override="", ent_id_override=""):
        """Shorthand to get message result."""

        if format_override == "":
            format_override = self.unbox_type_key

        result = self.do_execution(
            ent_id=ent_id_override,
            entity_attrs={"file_format": format_override},
            data_in=[("content", loaded_cart)],
            verify_input_content=False,
        )
        print(result)
        return result.get(
            self.unbox_result_key,
        )

    def complete_error_and_optout_test(
        self,
        loaded_cart: bytes,
        expected_error_msg: str = "",
        opt_out_type_override="BENIGN",
    ):
        """Run tests to ensure the unbox module opts out and fails when file type doesn't match what it can accept."""
        # Ensure optout with no entity type
        result = self.get_result_from_cart(loaded_cart, format_override=opt_out_type_override)
        self.assertEqual(result.state.label, State.Label.OPT_OUT)

        # Force through incorrect file and check if fails
        result = self.get_result_from_cart(loaded_cart, ent_id_override="not_a_test_entity_to_allow_type_override")
        if expected_error_msg == "":
            result.state.message = ""
        self.assertJobResult(
            result,
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message=expected_error_msg)),
        )

    def complete_double_optout_test(self, loaded_cart: bytes, opt_out_type_override="BENIGN"):
        """Run tests to ensure the unbox module opts out and fails when file type doesn't match what it can accept."""
        # Ensure optout with no entity type
        result = self.get_result_from_cart(loaded_cart, format_override=opt_out_type_override)
        self.assertEqual(result.state.label, State.Label.OPT_OUT)
        # Force through incorrect file and still opts out
        # self.assertJobResult(self.get_result_from_cart(loaded_cart), JobResult(state=State(State.Label.OPT_OUT)))
        result = self.get_result_from_cart(loaded_cart)
        self.assertEqual(result.state.label, State.Label.OPT_OUT)
