# -*- coding: utf-8 -*-.

"""
pygsheets.pivottable
~~~~~~~~~~~~~~

This module represents a pivottable within the worksheet.

"""

from pygsheets.utils import format_addr
from pygsheets.cell import Cell
from pygsheets.custom_types import ChartType
from pygsheets.exceptions import InvalidArgumentValue


class PivotTable(object):
    """
    PivotTables exist within a range of cells exhibiting mathematical groupings of the data within
    the cells. This could be an aggregation of specific rows. This could be a count of specific data
    within the cells. The PivotTable acts as a window or statistical display of the given data.

    :param worksheet:       Worksheet object in which the chart resides
    :param domain:          Cell range of the desired chart domain in the form of tuple of tuples
    :param ranges:          Cell ranges of the desired ranges in the form of list of tuple of tuples
    :param chart_type:      An instance of :class:`ChartType` Enum.
    :param title:           Title of the chart
    :param anchor_cell:     Position of the left corner of the chart in the form of cell address or cell object
    :param json_obj:      Represents a json structure of the chart as given in `api <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#BasicChartSpec>`__.


    >>> pivot = PivotTable(start='A1', end='B2', worksheet=wks)
    TODO
    >>> pivot.name = "my_named_range" # make this pivottable a named pivottable
    TODO
    >>> pivot.domain = ("A1", "B2") # Change the domain of the pivot table
    TODO
    >>> pivot.range = ("A1", "B2") # Change the range of the pivot table
    TODO
    >>> pivot.criteria = lambda x : x # Change the criteria of the pivot table
    TODO


    """

    def __init__(
        self,
        worksheet,
        domain=None,
        ranges=None,
        criteria=None,
        name="",
        anchor_cell=None,
        json_obj=None,
    ):
        self._name = name
        self._criteria = criteria
        self._domain = ()
        if domain:
            self._domain = (
                format_addr(domain[0], "tuple"),
                format_addr(domain[1], "tuple"),
            )
        self._ranges = []
        if ranges:
            for i in range(len(ranges)):
                self._ranges.append(
                    (
                        format_addr(ranges[i][0], "tuple"),
                        format_addr(ranges[i][1], "tuple"),
                    )
                )
        self._worksheet = worksheet
        self._pivot_table_id = None
        self._anchor_cell = anchor_cell
        if json_obj is None:
            self._create_pivot_table()
        else:
            self.set_json(json_obj)

    @property
    def name(self):
        """name of the pivot table"""
        return self._name

    @name.setter
    def name(self, new_name):
        temp = self._name
        self._name = new_name
        try:
            self.update_pivot_table()
        except:
            self._title = temp

    @property
    def domain(self):
        """
        Domain of the pivot table.
        The domain takes the cell range in the form of tuple of cell adresses. Where first adress is the
        top cell of the column and 2nd element the last adress of the column.

        Example: ((1,1),(6,1)) or ('A1','A6')
        """
        return self._domain

    @domain.setter
    def domain(self, new_domain):
        new_domain = (
            format_addr(new_domain[0], "tuple"),
            format_addr(new_domain[1], "tuple"),
        )
        temp = self._domain
        self._domain = new_domain
        try:
            self.update_pivot_table()
        except:
            self._domain = temp

    @property
    def criteria(self):
        """
        The criteria of the pivot table. Should be a numeral
        """
        return self._criteria

    @criteria.setter
    def criteria(self, new_chart_type):
        temp = self._chart_type
        self._chart_type = new_chart_type
        try:
            self.update_pivot_table()
        except:
            self._chart_type = temp

    @property
    def ranges(self):
        """
        Ranges of the chart (y values)
        A chart can have multiple columns as range. So you can provide them as a list. The ranges are
        taken in the form of list of tuple of cell adresses. where each tuple inside the list represents
        a column as staring and ending cell.

        Example:
            [((1,2),(6,2)), ((1,3),(6,3))] or [('B1','B6'), ('C1','C6')]
        """
        return self._ranges

    @ranges.setter
    def ranges(self, new_ranges):
        if type(new_ranges) is tuple:
            new_ranges = [new_ranges]

        for i in range(len(new_ranges)):
            new_ranges[i] = (
                format_addr(new_ranges[i][0], "tuple"),
                format_addr(new_ranges[i][1], "tuple"),
            )

        temp = self._ranges
        self._ranges = new_ranges
        try:
            self.update_chart()
        except:
            self._ranges = temp

    @property
    def id(self):
        """Id of the this chart."""
        return self._chart_id

    @property
    def anchor_cell(self):
        """Position of the left corner of the chart in the form of cell address or cell object,
        Changing this will move the chart.
        """
        return self._anchor_cell

    @anchor_cell.setter
    def anchor_cell(self, new_anchor_cell):
        temp = self._anchor_cell
        try:
            if type(new_anchor_cell) is Cell:
                self._anchor_cell = (new_anchor_cell.row, new_anchor_cell.col)
                self._update_position()
            else:
                self._anchor_cell = format_addr(new_anchor_cell, "tuple")
                self._update_position()
        except:
            self._anchor_cell = temp

    # TODO
    def delete(self):
        """
        Deletes the chart.

        .. warning::
            Once the chart is deleted the objects of that chart still exist and should not be used.
        """
        request = {"deleteEmbeddedObject": {"objectId": self._chart_id}}
        self._worksheet.client.sheet.batch_update(
            self._worksheet.spreadsheet.id, request
        )

    # TODO
    def refresh(self):
        """Refreshes the object to incorporate the changes made in the chart through other objects or Google sheet"""
        chart_data = self._worksheet.client.sheet.get(
            self._worksheet.spreadsheet.id, fields="sheets(charts,properties)"
        )
        sheet_list = chart_data.get("sheets")
        for sheet in sheet_list:
            if sheet.get("properties", {}).get("sheetId", None) is self._worksheet.id:
                chart_list = sheet.get("charts")
                if chart_list:
                    for chart in chart_list:
                        if chart.get("chartId") == self._chart_id:
                            self.set_json(chart)

    def _get_anchor_cell(self):
        if self._anchor_cell is None:
            if self._domain:
                return {
                    "columnIndex": self._domain[1][1] - 1,
                    "rowIndex": self._domain[1][0],
                    "sheetId": self._worksheet.id,
                }
            else:
                return {"columnIndex": 0, "rowIndex": 0, "sheetId": self._worksheet.id}

        else:
            if type(self._anchor_cell) is Cell:
                return {
                    "columnIndex": self._anchor_cell.col - 1,
                    "rowIndex": self._anchor_cell.row - 1,
                    "sheetId": self._worksheet.id,
                }
            else:
                cell = format_addr(self._anchor_cell, "tuple")
                return {
                    "columnIndex": cell[1] - 1,
                    "rowIndex": cell[0] - 1,
                    "sheetId": self._worksheet.id,
                }

    # TODO
    def _get_ranges_request(self):
        ranges_request_list = []
        for i in range(len(self._ranges)):
            req = {
                "series": {
                    "sourceRange": {
                        "sources": [
                            self._worksheet.get_gridrange(
                                self._ranges[i][0], self._ranges[i][1]
                            )
                        ]
                    }
                },
            }
            ranges_request_list.append(req)
        return ranges_request_list

    # TODO
    def _create_pivot_table(self):
        domains = []
        if self._domain:
            domains.append(
                {
                    "domain": {
                        "sourceRange": {
                            "sources": [
                                self._worksheet.get_gridrange(
                                    self._domain[0], self._domain[1]
                                )
                            ]
                        }
                    }
                }
            )

        request = {
            "addChart": {
                "chart": {
                    "spec": {
                        "title": self._title,
                        "basicChart": {
                            "chartType": self._chart_type.value,
                            "domains": domains,
                            "series": self._get_ranges_request(),
                        },
                    },
                    "position": {
                        "overlayPosition": {"anchorCell": self._get_anchor_cell()}
                    },
                }
            }
        }
        response = self._worksheet.client.sheet.batch_update(
            self._worksheet.spreadsheet.id, request
        )
        chart_data_list = response.get("replies")
        chart_json = chart_data_list[0].get("addChart", {}).get("chart")
        self.set_json(chart_json)

    # TODO
    def _update_position(self):
        request = {
            "updateEmbeddedObjectPosition": {
                "objectId": self._chart_id,
                "newPosition": {
                    "overlayPosition": {
                        "anchorCell": {
                            "sheetId": self._worksheet.id,
                            "rowIndex": self._anchor_cell[0] - 1,
                            "columnIndex": self._anchor_cell[1] - 1,
                        }
                    }
                },
                "fields": "*",
            }
        }
        self._worksheet.client.sheet.batch_update(
            self._worksheet.spreadsheet.id, request
        )

    # TODO
    def update_pivot_table(self):
        """updates the applied changes to the sheet."""
        request = {
            "updateChartSpec": {"chartId": self._chart_id, "spec": self.get_json()}
        }
        self._worksheet.client.sheet.batch_update(
            self._worksheet.spreadsheet.id, request
        )

    def get_json(self):
        """Returns the chart as a dictionary structured like the Google Sheets API v4."""

        domains = [
            {
                "domain": {
                    "sourceRange": {
                        "sources": [
                            self._worksheet.get_gridrange(
                                self._domain[0], self._domain[1]
                            )
                        ]
                    }
                }
            }
        ]
        ranges = self._get_ranges_request()
        spec = dict()
        spec["title"] = self._title
        spec["basicChart"] = dict()
        spec["titleTextFormat"] = dict()
        spec["basicChart"]["chartType"] = self._chart_type.value
        spec["basicChart"]["legendPosition"] = self._legend_position
        spec["titleTextFormat"]["fontFamily"] = self._title_font_family
        spec["fontName"] = self._font_name
        spec["basicChart"]["domains"] = domains
        spec["basicChart"]["series"] = ranges
        return spec

    # TODO
    def set_json(self, chart_data):
        """
        Reads a json-dictionary returned by the Google Sheets API v4 and initialize all the properties from it.

        :param chart_data:   The chart data as json specified in sheets api.
        """
        anchor_cell_data = (
            chart_data.get("position", {}).get("overlayPosition", {}).get("anchorCell")
        )
        self._anchor_cell = (
            anchor_cell_data.get("rowIndex", 0) + 1,
            anchor_cell_data.get("columnIndex", 0) + 1,
        )
        self._title = chart_data.get("spec", {}).get("title", None)
        self._chart_id = chart_data.get("chartId", None)
        self._title_font_family = (
            chart_data.get("spec", {})
            .get("titleTextFormat", {})
            .get("fontFamily", None)
        )
        self._font_name = (
            chart_data.get("spec", {})
            .get("titleTextFormat", {})
            .get("fontFamily", None)
        )
        basic_chart = chart_data.get("spec", {}).get("basicChart", None)
        self._chart_type = ChartType(basic_chart.get("chartType", None))
        self._legend_position = basic_chart.get("legendPosition", None)
        domain_list = basic_chart.get("domains", [])
        for d in domain_list:
            source_list = (
                d.get("domain", {}).get("sourceRange", {}).get("sources", None)
            )
            for source in source_list:
                start_row = source.get("startRowIndex", 0)
                end_row = source.get("endRowIndex", 0)
                start_column = source.get("startColumnIndex", 0)
                end_column = source.get("endColumnIndex", 0)
                self._domain = [
                    (start_row + 1, start_column + 1),
                    (end_row, end_column),
                ]
        range_list = basic_chart.get("series", [])
        self._ranges = []
        for r in range_list:
            source_list = (
                r.get("series", {}).get("sourceRange", {}).get("sources", None)
            )
            for source in source_list:
                start_row = source.get("startRowIndex", 0)
                end_row = source.get("endRowIndex", 0)
                start_column = source.get("startColumnIndex", 0)
                end_column = source.get("endColumnIndex", 0)
                self._ranges.append(
                    [(start_row + 1, start_column + 1), (end_row, end_column)]
                )

    # TODO
    def __repr__(self):
        return "<%s %s %s>" % (
            self.__class__.__name__,
            self.criteria,
            repr(self.name),
        )
