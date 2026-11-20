"""Exercise the real BRE source block and its CSV export with artificial data.

No raw survey data or full preprocessor execution is required. Only the actual
capacity statements and final export call are selected from the source AST;
the export destination is redirected to a temporary file.
"""
import ast
import copy
import io
from pathlib import Path
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = next(p for p in (ROOT/'breitenerhebung/dataPreprocessingBE.py',
                          ROOT/'data_preprocessing/breitenerhebung/dataPreprocessingBE.py') if p.exists())


def capacity_assignment(node):
    return isinstance(node, ast.Assign) and any(
        isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant)
        and t.slice.value == 'thermal_capacitance' for t in node.targets)


def source_block(destination, omit_encoding=False):
    tree = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
    start = next(i for i, node in enumerate(tree.body) if capacity_assignment(node))
    end = next(i for i, node in enumerate(tree.body) if i > start and capacity_assignment(node)
               and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute)
               and node.value.func.attr == 'astype')
    statements = copy.deepcopy(tree.body[start:end+1])
    if omit_encoding:
        statements = [node for node in statements if not (
            isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
            and any(isinstance(arg, ast.Name) and arg.id == 'cleanup_thermal_capacitance_encode'
                    for arg in node.value.args))]
    export = next(copy.deepcopy(node) for node in tree.body if isinstance(node, ast.Expr)
                  and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute)
                  and node.value.func.attr == 'to_csv')
    export.value.args[0] = ast.Constant(str(destination))
    module = ast.fix_missing_locations(ast.Module(body=statements+[export], type_ignores=[]))
    return compile(module, str(SOURCE), 'exec')


def execute_codes(codes, destination, omit_encoding=False):
    raw = pd.DataFrame({'scr_gebaeude_id': [f'TEST_{i}' for i in range(len(codes))],
                        'aw_konstr_1': codes})
    building = pd.DataFrame({'scr_gebaeude_id': raw.scr_gebaeude_id,
                             'unchanged_marker': list(range(len(codes)))})
    namespace = dict(pd=pd, be_data_original=raw, building_data=building)
    exec(source_block(destination, omit_encoding), namespace)
    return namespace['building_data']


class BRECapacitanceTests(unittest.TestCase):
    def test_all_documented_codes_roundtrip_as_physical_integers(self):
        expected = {'1':260000,'1.0':260000,'1.1':165000,'1.11':165000,
                    '1.2':260000,'1.3':260000,'1.4':260000,'1.5':260000,
                    '2':110000,'2.0':110000,'2.1':110000,'2.2':110000,'2.3':110000,
                    '3':165000,'3.0':165000,'3.1':165000,'3.2':165000,'3.3':165000,'3.4':165000}
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'result.csv'
            result = execute_codes(list(expected), output)
            saved = pd.read_csv(output, sep=';')
        self.assertEqual(result.thermal_capacitance.tolist(), list(expected.values()))
        self.assertEqual(saved.thermal_capacitance.tolist(), list(expected.values()))
        self.assertEqual(str(saved.thermal_capacitance.dtype), 'int64')
        self.assertEqual(saved.unchanged_marker.tolist(), list(range(len(expected))))

    def test_numeric_codes_from_excel_or_r_are_translated(self):
        with tempfile.TemporaryDirectory() as temp:
            result = execute_codes([1,1.0,1.1,1.11,1.2,2,2.0,2.1,3.4], Path(temp)/'result.csv')
        self.assertEqual(result.thermal_capacitance.tolist(),
                         [260000,260000,165000,165000,260000,110000,110000,110000,165000])

    def test_unknown_or_missing_codes_block_export(self):
        for invalid in (None, float('nan'), '', 'nan', '1.99', 'unknown', 999):
            with self.subTest(value=str(invalid)), tempfile.TemporaryDirectory() as temp:
                output = Path(temp)/'result.csv'
                with self.assertRaisesRegex(ValueError, 'thermal_capacitance'):
                    execute_codes(['1.2',invalid], output)
                self.assertFalse(output.exists())

    def test_processed_capacities_are_not_accepted_as_raw_construction_codes(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'result.csv'
            with self.assertRaises(ValueError): execute_codes([165000], output)
            self.assertFalse(output.exists())

    def test_missing_first_mapping_call_is_caught_before_export(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'result.csv'
            with self.assertRaisesRegex(ValueError, 'thermal_capacitance'):
                execute_codes(['1.2'], output, omit_encoding=True)
            self.assertFalse(output.exists())

    def test_explicit_numeric_output_with_future_pandas_replace_behavior(self):
        try: pd.get_option('future.no_silent_downcasting')
        except pd.errors.OptionError: self.skipTest('Option not available in this pandas version')
        with pd.option_context('future.no_silent_downcasting', True), tempfile.TemporaryDirectory() as temp:
            result = execute_codes(['1.2','2.1','3.1'], Path(temp)/'result.csv')
        self.assertEqual(str(result.thermal_capacitance.dtype), 'int64')

    def test_restored_preprocessor_is_python_and_warning_import_is_public(self):
        source = SOURCE.read_text(encoding='utf-8-sig')
        compile(source, str(SOURCE), 'exec')
        self.assertNotIn('<!DOCTYPE html>', source[:200])
        namespace = {}
        exec('from pandas.errors import SettingWithCopyWarning', namespace)
        self.assertIn('SettingWithCopyWarning', namespace)


if __name__ == '__main__': unittest.main()
