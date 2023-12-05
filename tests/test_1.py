from orh.core.html import get_base_url, get_tree

source = """



        <!DOCTYPE html>
        <html web-base-url="http://localhost:8069">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="initial-scale=1"/>
                <title>Odoo Report</title>
                <link type="text/css" rel="stylesheet" href="report_assets_common.css"/>
                <script type="text/javascript" src="assets_common.js"></script>
                <script type="text/javascript" src="report_assets_common.js"></script>




        </head>
            <body class="container">
                <div id="wrapwrap">
                    <main>
                    </main>
                </div>
            </body>
        </html>
"""


def test_base_url():
    tree = get_tree(source)
    base_url, tree = get_base_url(tree)

    #     html = """
    # <html web-base-url="http://localhost:8069">
    #             <head>
    #                 <meta charset="utf-8"/>
    #                 <meta name="viewport" content="initial-scale=1"/>
    #                 <title>Odoo Report</title>
    #                 </head>
    #             <body class="container">
    #                 <div id="wrapwrap">
    #                     <main>
    #                     </main>
    #                 </div>
    #             </body>
    #         </html>
    # """

    assert base_url == "http://localhost:8069"
    # assert tree == get_tree(html)


# def test_header():
#     tree = get_tree(source)
#     res, tree = get_header(tree)

#     print(tree_to_string(tree))

#     assert len(res) == 2
#     assert "text/css" in res
#     assert "text/javascript" in res
