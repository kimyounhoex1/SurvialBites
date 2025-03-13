function signupAction() {
  const name = $("#signup_name_input").val();
  const id = $("#signup_id_input").val();
  const pw = $("#signup_pw_input").val();

  $.ajax({
    type: "POST",
    url: "/signup",
    contentType: "application/json",
    data: JSON.stringify({ id: id, pw: pw, name: name }),
    success: function (response) {
      console.log(response);
    },
  });
}

function loginAction() {
  const id = $("#login_id_input").val();
  const pw = $("#login_pw_input").val();
  $.ajax({
    type: "POST",
    url: "/login",
    contentType: "application/json",
    data: JSON.stringify({ id: id, pw: pw }),
    success: function (response) {
        if(response['result'] == 'failure'){
          alert(response['message'])
          // window.location.href="/loginpage?redirect=" + response["redirectUri"]
        }
        else
          window.location.href="/mainpage";

      // sessionStorage.setItem("jwtToken", response["token"]);
      // console.log("토큰이 저장되었습니다.");

    },
  });
}
