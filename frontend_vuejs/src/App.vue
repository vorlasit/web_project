<template> 
  <router-view />
</template>
 <style>
body.dark-mode {
  background-color: #121212;
  color: #ffffff;
}

body.dark-mode .card {
  background-color: #1e1e1e;
  color: #ffffff;
}

body.dark-mode .navbar {
  background-color: #000 !important;
}

body.dark-mode .dropdown-menu {
  background-color: #1e1e1e;
  color: white;
}

body.dark-mode .dropdown-item {
  color: white;
}

body.dark-mode .dropdown-item:hover {
  background-color: #333;
}
</style>