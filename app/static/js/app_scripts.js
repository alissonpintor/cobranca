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


/**
 *  Controle das Tasks em execução
 */

var taskModel = (function(){
    /**
     * Representa a model que vai conter todos os objetos das tarefas
     * em execução no backend
     */
    
    var Task = function (taskId, total, current, status) {
        this.id = taskId;
        this.total = total;
        this.current = current;
        this.status = status;
    };

    var task;

    return {
        // 1) criar Task
        createTask: function (data) {
            task = new Task(
                data.id,
                data.total,
                data.current,
                data.status
            )
        },

        // 2) update task
        updateTask: function (current, status) {
            task.current = current;
            task.status = status;
        },

        // 3) get task
        getTask: function () {
            return task;
        }
    }
 });

 var taskUI = (function(){
     var elements = {
        taskTitle: document.getElementById('task-title'),
        taskPanel: document.getElementById('task-panel'),
        taskMessage: document.getElementById('task-message'),
        progressBar: document.getElementById('task-progress-bar')
     }

     return {
         updateTaskHTML: function (task) {
            var currentPerc = parseInt((parseInt(task.current) * 100) / parseInt(task.total));

            elements.taskMessage.innerHTML = `
                <strong>Tarefas Executadas: </strong> &#32; ${task.current} &#32; de &#32; ${task.total} &#32;
                <strong>Status: </strong> &#32; ${task.status} &#32;
            `;
            
            elements.progressBar.style.width = `${currentPerc}%`;
            elements.progressBar.innerHTML = `${currentPerc}%`;
         },

         addButton: function () {
             var button = document.createElement('a');
             button.href = window.location.pathname + '?clear_task=yes';
             button.innerHTML = 'Atualizar Pagina';
             button.classList.add('btn', 'btn-primary');

             elements.taskPanel.insertAdjacentElement('beforeend', button);
         },

         updateTitleText: function (text) {
            elements.taskTitle.innerText = text;
         }
     }
 });

 var taskControl = (function(){
     var model = taskModel();
     var ui = taskUI();
    
     // 1) iniciar a task a partir do id
     var initTask = function (taskId) {
        $.ajax({
            url: `/financeiro/task/${taskId}`,
            success: (data) => {
                model.createTask(data);
                updateTasks();
            }
        });
     };

     // 2) atualizar o status da task
     var updateTasks = function () {
         var task = model.getTask();
         ui.updateTaskHTML(task);

         if (task.current < task.total) {
             setTimeout( () => {
                $.ajax({
                    url: `/financeiro/task/${task.id}`,
                    success: (data) => {
                        model.updateTask(data.current, data.status)
                        updateTasks();
                    }
                });
             }, 1000);
         } else {
            ui.addButton();
            ui.updateTitleText('Tarefa Completada');
         }
     };

     // 3) exibir tarefa finalizada quando a task for encerrada

     return {
         init: function (taskId) {
            initTask(taskId);
            // model.createTask(data);
         }
     }
 });