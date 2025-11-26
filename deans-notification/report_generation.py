import os
from pyreportjasper import JasperPy

def compiling():
    template = os.path.dirname(os.path.abspath(__file__)) + \
                 '/jasper/crisis_report_template.jrxml'
    jasper = JasperPy()
    jasper.compile(template)

def json_to_pdf(report_count):
    template = os.path.dirname(os.path.abspath(__file__)) + \
                 '/jasper/crisis_report_template.jrxml'

    output = os.path.dirname(os.path.abspath(__file__)) + '/reports/report'+str(report_count)
    json_query = 'cases'

    data_file = os.path.dirname(os.path.abspath(__file__)) + \
        '/json_summary/json'+str(report_count)+'.json'

    jasper = JasperPy()
    jasper.process(
        template,
        output_file=output,
        format_list=["pdf"],
        parameters={},
        db_connection={
            'data_file': data_file,
            'driver': 'json',
            'json_query': json_query,
        },
        locale='en_US'
    )

    print('Result is the file below.')
    print(output + '.pdf')

if __name__ == '__main__':
    compiling()
    print('compiling complete')
    json_to_pdf()