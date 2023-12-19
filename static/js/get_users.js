const fetchEnv = async () => {
  try {
    const response = await fetch("/env");
    const config = await response.json();

    return config;
  } catch (error) {
    console.error("Error fetching configuration:", error);
  }
};

const loadUpdateForm = (userId) =>
  (window.location.href = `/update_user/${userId}`);

const deleteUser = async (userId) => {
  try {
    const config = await fetchEnv();

    if (confirm("Are you sure you want to delete this user?")) {
      $.ajax({
        type: "DELETE",
        url: `${config.API_URL}/users/${userId}`,

        success: (data) => {
          alert(data.message);
          location.reload();
        },
        error: (error) => {
          alert("Error deleting user: " + error.responseJSON.error);
        },
      });
    }
  } catch (error) {
    console.log("delete user error", error);
  }
};
