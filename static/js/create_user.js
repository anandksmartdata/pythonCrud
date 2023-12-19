const fetchEnv = async () => {
  try {
    const response = await fetch("/env");
    const config = await response.json();

    return config;
  } catch (error) {
    console.error("Error fetching configuration:", error);
  }
};

const createUser = async () => {
  try {
    const config = await fetchEnv();

    const formData = {
      firstName: $("#firstName").val(),
      lastName: $("#lastName").val(),
      email: $("#email").val(),
      age: $("#age").val(),
      password: $("#password").val(),
    };

    $.ajax({
      type: "POST",
      url: `${config.API_URL}/users`,
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify(formData),
      success: function (data) {
        alert(data.message);
        clearForm();
        // window.location.href = "{{ url_for('get_all_users') }}";
        window.location.href = "/users";
      },
      error: function (error) {
        alert("Error creating user: " + error.responseJSON.error);
      },
    });
  } catch (error) {
    console.log("create user error", error);
  }
};

const clearForm = () => {
  $("#firstName").val("");
  $("#lastName").val("");
  $("#email").val("");
  $("#age").val("");
  $("#password").val("");
};
