// load file 
$('#choose-file-icon').on('click', function () {
    $('input[name=dataset]').click()
})

// enable uploading btn after choosing a file
$('input[name=dataset]').on('change', function () {
    if ($(this).val() != '') $('#load-dataset-btn').removeAttr('disabled')
    else $('#load-dataset-btn').attr('disabled', 'disabled')
    // set filename
    $('#file-name').html($(this).val())
    $('#visual').html('')
})


// load dataset via ajax
$('#load-dataset-btn').click(function () {
    if ($('input[name=dataset]')[0].files[0] != undefined) {
        $('#file-upload-spinner').show()
        $('#load-dataset-btn').attr('disabled', 'disabled')
        $('input[name=dataset]').attr('disabled', 'disabled')

        var formData = new FormData();
        formData.append('dataset', $('input[name=dataset]')[0].files[0]);

        $.ajax({
            url: '/api/dataset/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                resetInputs()
                toastr.success('Dataset loaded successfuly', {
                    timeOut: 3000
                })
            },
            error: function (err) {
                resetInputs()
                $('#visual').html(err.responseJSON.visual)
                toastr.error(err.responseJSON.message ?? '', 'Some records are missing')
            }
        });
    }
})

// reset inputs after loading a file
function resetInputs() {
    $('#file-upload-spinner').hide()
    $('#load-dataset-btn').attr('disabled', 'disabled')
    $('input[name=dataset]').removeAttr('disabled')
    $('#file-name').html('')
    $('input[name=dataset]').val(null)
}