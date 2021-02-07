Parsers - HTML parser
=======================

.. automodule:: MordinezNLP.parsers.HTML_Parser
   :members:

Example usage for HTML files:

.. code:: python

        from MordinezNLP.parsers import HTML_Parser

        with open("my_html_file.html", "r") as f:
            html_content = HTML_Parser(f.read())
            print(html_content)
