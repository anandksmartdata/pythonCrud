const fetchEnv = async () => {
  try {
    const response = await fetch("/env");
    const config = await response.json();

    return config;
  } catch (error) {
    console.error("Error fetching configuration:", error);
  }
};

const userId = window.location.pathname.split("/").pop();

const loadUserData = async () => {
  try {
    const config = await fetchEnv();

    $.ajax({
      type: "GET",
      url: `${config.API_URL}/users/${userId}`,
      
      success: function (data) {
        $("#firstName").val(data?.user?.firstName);
        $("#lastName").val(data?.user?.lastName);
        $("#email").val(data?.user?.email);
        $("#age").val(data?.user?.age);
      },
      error: function (error) {
        console.log(error);
        alert("Error loading user data: " + error?.responseJSON?.error);
      },
    });
  } catch (error) {
    console.log("load user error", error);
  }
};

const updateUser = async () => {
  try {
    const config = await fetchEnv();

    const formData = {
      firstName: $("#firstName").val(),
      lastName: $("#lastName").val(),
      email: $("#email").val(),
      age: $("#age").val(),
    };

    $.ajax({
      type: "PUT",
      url: `${config.API_URL}/users/${userId}`,
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify(formData),
      success: (data) => {
        alert(data?.message);
        // window.location.href = "{{ url_for('get_all_users') }}";
        window.location.href = "/users";
      },
      error: (error) =>
        alert("Error updating user: " + error?.responseJSON?.error),
    });
  } catch (error) {
    console.log("update user error: " + error);
  }
};

$(document).ready(() => loadUserData());
