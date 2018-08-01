from flask_assets import Bundle


css = Bundle(
    'css/bootstrap.min.css',
    'css/bootstrap-multiselect.css',
    'css/bootstrap-datetimepicker.min.css',
    'css/bootstrap-table.min.css',
    'css/bootstrap-editable.css',
    'http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700',
    'css/demo.min.css',
    'css/dashboard.css',
    'css/styles.css'
)


js = Bundle(
    'js/moment-with-locales.js',
    'js/jquery.min.js',
    'js/resizer.js',
    'js/jquery-ui.min.js',
    'js/jquery.slimscroll.min.js',
    'js/jquery.inputmask.min.js',
    'js/switchery.min.js',
    'js/bootstrap.min.js',
    'js/bootstrap-multiselect.js',
    'js/bootstrap-datetimepicker.min.js',
    'js/bootstrap-table.min.js',
    'js/bootstrap-table-pt-BR.js',
    'js/bootstrap-table-editable.js',
    'js/bootstrap-editable.min.js',
    'js/bootstrap-table-reorder-columns.js',
    'js/libs/FileSaver/FileSaver.min.js',
    'js/libs/js-xlsx/xlsx.core.min.js',
    'js/libs/jsPDF/jspdf.min.js',
    'js/libs/jsPDF-AutoTable/jspdf.plugin.autotable.js',
    'js/bootstrap-table-export.js',
    'js/tableExport.min.js',
    'js/jquery.dragtable.js',
    'js/notify.js',
    'js/ultra.js',
    'js/demo.js',
    'js/init.js',
    'js/app_scripts.js'
    #filters='jsmin',
    #output='gen/packed.js'
)
