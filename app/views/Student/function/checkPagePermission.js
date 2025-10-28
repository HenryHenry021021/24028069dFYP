// static/js/auth.js
(function () {
    // Helper to read cookies
    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
    }
  
    const userId = getCookie("user_id");
    const role = getCookie("role");
  
    // Check if user_id is missing
    if (!userId) {
      alert("Please log in first.");
      window.location.href = window.location.origin + "/";
            return;
    }
  
    // Check if role is not student
    if (role !== "1") {
      alert("Access denied. Only students are allowed here.");
      window.location.href = window.location.origin + "/";
      return;
    }
  })();
  