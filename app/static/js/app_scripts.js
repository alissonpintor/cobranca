$(function () {

    // Adiciona as mascaras para os inputs que possuirem
    // um valor para input-mask
    $(":input").inputmask();


    // Inicializa o inputs de acordo com o tipo
    inicializa_inputs();

    // makes sure the whole site is loaded
    $(window).on('load', function() {
        $("#content").show();
        $("#loading").delay(1000).fadeOut("slow");
    })

    // makes sure the whole site is unloaded
    $(window).on('beforeunload', function(event) {
        $("#loading").fadeIn("slow");
    })

});


function inicializa_inputs(){
    /* 
        Inicializa os frameworks utilizados pelos inputs
        Atraves do atributo data-type
        
        tipos de data-type:
            @date: datepicker
            @datetime: datepicker
    */

    // Inicializa o inputs de acordo com o tipo
    $(":input").each((index, obj) => {
        var type = $(obj).data("type");
        
        // Verfifica se e undifined
        if (type) {
            // Se for do tipo date inicializa o datepicker
            if (type === "date") {
                $( obj ).datepicker({
                    format: 'dd/mm/yyyy',
                    locale: 'pt-br'
                });

                $(obj).inputmask("dd/mm/yyyy");
            }

            // Se for do tipo datetime inicializa o datepicker
            if (type === "datetime") {
                $( obj ).datetimepicker({
                    format: 'dd/mm/yyyy hh:mm:ss',
                    locale: 'pt-br'
                });
            }

            if (type === 'multiselect') {
                $(obj).multiselect();
            }

            if (type === 'integer') {
                $(obj).inputmask({
                    mask: "9{10}",
                    greedy: false
                });
            }
        }
    });
}
/*
const LOCATIONS = {
    '/configuracoes/financeiro': () => {
        configCobrancaControl.init();
    }
}

var configCobrancaControl = (function(){
    
    return {
        init: function() {
            console.log('deu certo', '/configuracoes/financeiro');
        }
    }
})();
*/

/*
var cobrancaControl = (function(){
    var dataInicial, dataFinal, DOM, errors;
    errors = []

    DOM = {
        dtinicial: '#dtinicial',
        dtfinal: '#dtfinal',
        buscar: '#buscar',
        enviar: '#enviar',
        errors: '#errors'
    };

    var formatDate = function(data) {
        var splitDate, year, month, day, formatedDate;
        if (data) {
            splitDate = data.split('/');

            year = parseInt(splitDate[2]);
            month = parseInt(splitDate[1]) - 1;
            day = parseInt(splitDate[0]);
            
            formatedDate = new Date(year, month, day);

            return formatedDate;
        } else {
            return undefined;
        }     
    };

    var showErrors = function() {
        var html, htmlErrors;
        htmlErrors = '';
        
        html = '<div class="alert alert-danger" role="alert">' +
               '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
               '<ul>' +
               '#errors#' +
               '</ul>' +
               '</div>';
        
        $(errors).each(function(index, error){
            htmlErrors += '<li>' + error + '</li>';
        });

        html = html.replace('#errors#', htmlErrors);
        errors = [];

        $(DOM.errors).html(html);
        //$(DOM.errors).toggle('fade');
    };

    var validate = function() {
        var today = new Date();
        today.setHours(0,0,0,0);

        if (dataInicial === undefined) {
            errors.push('A data inicial é obigatório.');
        }

        if (dataFinal === undefined) {
            errors.push('A data final é obigatório.');
        }

        if (dataInicial > dataFinal) {
            errors.push('A data inicial deve ser menor que a final.');
        }

        if (dataFinal >= today) {
            errors.push('A data final deve ser menor que hoje.');
        }
    };

    var setEvents = function() {
        $(DOM.buscar).on('click', function(event){
            event.preventDefault();

            dataInicial = formatDate($(DOM.dtinicial).val());
            dataFinal = formatDate($(DOM.dtfinal).val());

            validate();
            if (errors) {
                showErrors();
            }

            //console.log(dataInicial > dataFinal);
            //console.log(dataInicial.toLocaleDateString());
        })
    };

    return {
        init: function() {
            setEvents();
        },

        data: function() {
            return {
                dtinicial: dataInicial,
                dtfinal: dataFinal
            }
        }
    };
})(); */