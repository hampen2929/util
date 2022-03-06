from datetime import datetime
from typing import Any, List

import pytest
from _pytest.runner import CallInfo
from py.xml import html
from pytest_html.plugin import HTMLReport

from util.test import docstring_parser


def pytest_html_report_title(report: HTMLReport) -> None:
    report.title = "util"


def pytest_configure(config: Any) -> None:
    print("===============")
    print(type(config))
    print("===============")
    if not hasattr(config, "_metadata"):
        raise AttributeError("config doesn't have attribute _metadata")
    config._metadata["Version"] = "0.0.1"


def pytest_html_results_table_header(cells: List[Any]) -> None:
    del cells[1:]
    cells.insert(0, html.th("Module"))
    cells.insert(1, html.th("Tests"))
    cells.insert(2, html.th("Expects"))
    cells.append(html.th("Time", class_="sortable time", col="time"))


def pytest_html_results_table_row(report: HTMLReport, cells: List) -> None:
    del cells[1:]
    cells.insert(0, html.td(report.moduleName))
    cells.insert(1, html.td(report.tests))
    cells.insert(2, html.td(report.expects))
    cells.append(html.td(str(datetime.now()), class_="col-time"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: CallInfo) -> Any:
    outcome = yield
    report = outcome.get_result()
    docstring = docstring_parser.parse(str(item.function.__doc__))
    report.moduleName = docstring["Module"] if "Module" in docstring else "Module is not entered"
    report.tests = docstring["Tests"] if "Tests" in docstring else "Tests is not entered"
    report.expects = docstring["Expects"] if "Expects" in docstring else "Expects is not entered"
