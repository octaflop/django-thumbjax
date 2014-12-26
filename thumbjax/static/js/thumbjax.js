// Requires jquery
$(document).ready(function() {

  // Secure Ajax for Django
  var csrftoken = $.cookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      // Sending for all...
      if (!csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // var jaxerapiurl = "{% url thumbjax:api:index %}";
  var jaxerapiurl = '/thumbjax/api/'

  $.each($('img.thumbj'), function(i, img){
    var poller = {
      // num of failed reqs
      failed: 0,

      // starting interval
      interval: 1000,

      // task id
      taskid: '',

      // taskurl
      taskurl: '',

      // our init timeout
      init: function(taskid) {
        if (this.failed <= 10) {
          this.taskid = taskid;
          this.taskurl = "/task/status/" + taskid + "/";
          // console.log("Current interval: " + this.interval);
          setTimeout($.proxy(this.getData, this), this.interval);
          this.interval += 500;
          this.failed += 1;
        } else {
          console.log('Tried too many times. Breaking out.');
        }
      },

      // our get function
      getData: function() {
        var self = this;

        $.ajax({
          url: this.taskurl,
          method: 'GET',
          dataType: 'json',
          cache: false,
          success: function(resp){
            if (resp.task.status === 'SUCCESS') {
              console.log('Successfully got result: ' + resp.task.result);
              $("img[data-taskid='"+resp.task.id+"']").attr('src', resp.task.result);
              $("img[data-taskid='"+resp.task.id+"']").removeClass('thumbj');
              $("img[data-taskid='"+resp.task.id+"']").addClass('thumbj-done');
              return(false);
            } if (resp.task.status === 'ERROR') {
              // just stop polling
            } else {
              self.init(resp.task.id);
            }
          },
          // gateway timeout, usually
          error: $.proxy(self.errorHandler, self)
        });
      },

      errorHandler: function() {
        if (++this.failed < 10) {
          this.interval += 1000;
          this.init(this.taskid);
        }
      }
    }

    var taskid = $(img).data('taskid');
    poller.init(taskid);

  });
});