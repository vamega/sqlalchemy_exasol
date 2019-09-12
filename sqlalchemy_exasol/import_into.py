from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.sql.base import _generative
from sqlalchemy.types import TypeEngine


class ImportInto(ClauseElement):
    __visit_name__ = "import_into"

    def __init__(
        self,
        # target_table,
        target_columns,  # type: dict[str, TypeEngine]
    ):
        # self._target_table = target_table
        self._target_columns = target_columns


def import_into(target_columns):
    return ImportInto(target_columns)


@compiles(ImportInto, "exasol")
def visit_merge(
    element,  # type: ImportInto
    compiler,
    **kw
):
    print("Entered visit_merge")
    import_columns = ", ".join(
        [
            "%s %s" % (column_name, compiler.process(column_type))
            for column_name, column_type in element._target_columns
        ]
    )
    msql = "IMPORT INTO (%s) " % compiler.process(element._target_table, asfrom=True)
    # msql += "USING %s " % compiler.process(element._source_expr,
    #                                        asfrom=True)
    # msql += "ON ( %s ) " % compiler.process(element._on)

    # if element._merge_update_values is not None:
    #     cols = crud._get_crud_params(compiler, element._merge_update_values)
    #     msql += "\nWHEN MATCHED THEN UPDATE SET "
    #     msql += ', '.join(compiler.visit_column(c[0]) + '=' + c[1] for c in cols)
    #     if element._merge_delete:
    #         msql += "\nDELETE "
    #         if element._delete_where is not None:
    #             msql += " WHERE %s" % compiler.process(element._delete_where)
    #     else:
    #         if element._update_where is not None:
    #             msql += " WHERE %s" % compiler.process(element._update_where)
    # else:
    #     if element._merge_delete:
    #         msql += "\nWHEN MATCHED THEN DELETE "
    #         if element._delete_where is not None:
    #             msql += "WHERE %s" % compiler.process(element._delete_where)
    # if element._merge_insert_values is not None:
    #     cols = crud._get_crud_params(compiler, element._merge_insert_values)
    #     msql += "\nWHEN NOT MATCHED THEN INSERT "
    #     msql += "(%s) " % ', '.join(compiler.visit_column(c[0]) for c in cols)
    #     msql += "VALUES (%s) " % ', '.join(c[1] for c in cols)
    #     if element._insert_where is not None:
    #         msql += "WHERE %s" % compiler.process(element._insert_where)

    return msql
