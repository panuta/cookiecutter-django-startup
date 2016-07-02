function _map_upload_error(error_message, uploader) {
  if(error_message == 'file-too-big') {
    return uploader.options.dictFileTooBig
  } else if(error_message == 'invalid-file-type') {
    return uploader.options.dictResponseError;
  } else if(error_message == 'max-files-exceeded') {
    return uploader.options.dictResponseError;
  } else if(error_message == 'response-error') {
    return uploader.options.dictResponseError;
  }

  return error_message;
}

function user_profile_uploader(element_selector, uploader_params, existing_image) {
  Dropzone.autoDiscover = false;

  var uploader = new Dropzone(element_selector, {
    url: uploader_params.upload_url,
    method: "post",
    paramName: 'file',
    maxFilesize: uploader_params.max_file_size,
    clickable: true,
    acceptedFiles: uploader_params.accepted_file,
    previewTemplate: document.getElementById('preview-template').innerHTML,

    dictRemoveFile: 'Remove',
    dictFileTooBig: "File is too big (limit " + uploader_params.max_file_size_in_mb + " MB)",
    dictInvalidFileType: 'Invalid file type',
    dictResponseError: 'Response error',
    dictCancelUpload: 'Cancel upload',
    dictMaxFilesExceeded: 'Max files exceeded',
    dictRemoveFileConfirmation: 'Confirm remove file?',

    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },

    init: function () {
      this.existingFileElement = undefined;

      if (existing_image) {
        var image = {
          name: existing_image.name,
          size: existing_image.size,
          status: 'Dropzone.ADDED',
          accepted: 'true'
        };

        this.emit('addedfile', image);
        this.emit('thumbnail', image, existing_image.url);
        this.emit('complete', image);
        this.files.push(image);

        this.existingFileElement = image.previewElement;

        image.previewElement.addEventListener('click', function () {
          uploader.hiddenFileInput.click();
        });
      }

      this.on('success', function (file, response, formData) {
        if (this.files.length > 1) {
          this.removeFile(this.files[0]);
        }

        file.previewElement.addEventListener('click', function () {
          uploader.hiddenFileInput.click();
        });
      });

      this.on('addedfile', function (file) {
        if (this.files.length) {
          this.existingFileElement = this.files[0].previewElement;

          if (this.files.length > 1) {
            $(this.existingFileElement).removeClass('dz-success').hide();
          }
        }
      });

      this.on('removedfile', function(file) {
        if (!this.files.length) {
          var jqxhr = $.post(uploader_params.delete_url, function(response) {

          });
        }
      });
    },
    error: function (file, message) {
      // Do not display new element when error, just show error message

      uploader.removeFile(file);
      showPageNotification('error', _map_upload_error(message, uploader));

      if(this.existingFileElement) {
        $(this.existingFileElement).show();
        this.existingFileElement = undefined;
      }

      return false;
    }
  });
}