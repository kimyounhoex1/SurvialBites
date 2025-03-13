$(document).ready(function () {
  $("#img-file").on("change", function () {
    var file = this.files[0];
    if (file) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#preview").attr("src", e.target.result).show();
      };
      reader.readAsDataURL(file);
    } else {
      $("#preview").hide();
    }
  });
});

function uploadPost() {
  let title = $("#title").val();
  let image = $("#img-file")[0].files[0];
  let content = $("#content").val();

  let foodtype = $("#foodtype").val();
  const selectedOption = document.querySelector('input[name="option"]:checked');
  let meetingtype = selectedOption.value;
  let appointment_time = $("#meeting").val();
  let max_of_participants = $("#max_of_participants").val();
  max_of_participants = parseInt(max_of_participants, 10);
  let current_participants = 0;

  let formData = new FormData();
  formData.append("title", title);
  formData.append("content", content);
  formData.append("foodtype", foodtype);
  formData.append("meetingtype", meetingtype);
  formData.append("appointment_time", appointment_time);
  formData.append("max_of_participants", max_of_participants);
  formData.append("current_participants", current_participants);

  if (image) {
    formData.append("file", image);
  }

  $.ajax({
    type: "POST",
    url: "/uploadPost",
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response["result"] != "success") {
        console.log("포스팅 실패!");
      } else {
        console.log("포스팅 성공!");
        window.location.href="/mainpage"
      }
    },
  });
}
