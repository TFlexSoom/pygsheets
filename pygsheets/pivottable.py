# -*- coding: utf-8 -*-.

"""
pygsheets.pivottable
~~~~~~~~~~~~~~

This module represents a pivottable within the worksheet.

"""
from enum import Enum

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
    :param rows:            Cell range of the desired row values in the form of tuple of tuples
    :param columns:         Cell range of the desired column values in the form of tuple of tuples
    :param values:          Cell range of the desired pivot table values
    :param source:          Cell range of the desired pivot table data
    :param layout:          Value of PivotValueLayout
    :param filter_specs:    TODO
    :param anchor_cell:     Position of the left corner of the chart in the form of cell address or cell object
    :param json_obj:        Represents a json structure of the chart as given in `api <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#BasicChartSpec>`__.

    >>> pivot = PivotTable(start='A1', end='B2', worksheet=wks)
    TODO
    >>> pivot.rows = ("A1", "B2") # Change the rows of the pivot table
    TODO
    >>> pivot.columns = ("A1", "B2") # Change the columns of the pivot table
    TODO
    >>>


    """
    pass


class PivotGroup(object):
    """
    PivotTables exist within a range of cells exhibiting mathematical groupings of the data within
    the cells. This could be an aggregation of specific rows. This could be a count of specific data
    within the cells. The PivotTable acts as a window or statistical display of the given data.

    :param source:          reference to the cell data for the grouping
    :param source_offset:   numerical offset of source for group data
    :param show_totals:     True if the pivot table should include totals for the row/column
    :param repeat_headings: True if the pivot table should repeat prefix groupings for row/column
    :param sort_order:      Value of SortOrder enum
    :param value_bucket:    TODO
    :param label:           String label
    :param group_rule:      TODO
    :param group_limit:     TODO
    :param metadata:        list of tuples detailing values in the pivot grouping. Check 
        `<https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#pivotgroupvaluemetadata>`__.
    :param json_obj:        Represents a json structure of the chart as given in `api 
        <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#BasicChartSpec>`__.

    """
    pass



class PivotGroupValueMetadata:
    # (value: any, collapsed: bool)
    pass

class PivotGroupSortValueBucket:
    # (valuesIndex: int, buckets: [any])
    pass

class PivotGroupRule:
    pass

class ManualRule(PivotGroupRule):
    # groups :: groups: [(groupName: any, items: [any])]
    pass

class HistogramRule(PivotGroupRule):
    # (interval: double, start: double, end: double)
    pass

class DateTimeRule(PivotGroupRule):
    # (type: DateTimeRuleType)
    pass

class PivotGroupLimit:
    # (countLimit: int, applyOrder: int)
    pass

class PivotFilterCriteria:
    # (visibleValues: [string], condition: BooleanCondition, visibleByDefault: bool)
    pass

class PivotFilterSpec:
    # (filterCriteria: PivotFilterCriteria, source :: columnOffsetIndex : int | dataSourceColumnReference: DataSourceColumnReference)
    pass

class PivotValue:
    # (
    ##  summarizeFunction: PivotValueSummarizeFunction, 
    ##  name: string,  
    ##  calculatedDisplayType: PivotValueCalculatedDisplayType, 
    ##  sourceColumnOffset: int,
    ##  formula: string,
    ##  dataSourceColumnReference: DataSourceColumnReference,
    # )
    pass

class PivotValueSummarizeFunction(Enum):
    SUM = "SUM"
    COUNTA = "COUNTA"
    COUNT = "COUNT"
    COUNTUNIQUE = "COUNTUNIQUE"
    AVERAGE = "AVERAGE"
    MAX = "MAX"
    MIN = "MIN"
    MEDIAN = "MEDIAN"
    PRODUCT = "PRODUCT"
    STDDEV = "STDDEV"
    STDDEVP = "STDDEVP"
    VAR = "VAR"
    VARP = "VARP"
    CUSTOM = "CUSTOM"

class PivotValueCalculatedDisplayType(Enum):
    PERCENT_OF_ROW_TOTAL = "PERCENT_OF_ROW_TOTAL"
    PERCENT_OF_COLUMN_TOTAL = "PERCENT_OF_COLUMN_TOTAL"
    PERCENT_OF_GRAND_TOTAL = "PERCENT_OF_GRAND_TOTAL"

class PivotValueLayout(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"
