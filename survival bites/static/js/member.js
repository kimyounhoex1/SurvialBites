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
      // 변경한 부분, 회원가입시 json 형식으로 성공 실패 확인
      if(response['result']== 'failure')
        alert(response['message'])
      else
        window.location.href="/loginpage"
      //
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

function openMyFunction() {
  $("#profile-container").toggle();
}

function logout() {
  $.ajax({
    url: '/logout',
    type: 'POST',
    success: function(response){
     if(response['result']!='failure'){
      console.log("로그아웃 성공")
      document.cookie = "jwtToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      window.location.href = "/loginpage"
     }
     else {
      console.log("로그아웃 실패")
     }
    }
  });
}
