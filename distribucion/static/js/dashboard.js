document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById('sidebar');

    // Si el ancho es menor a 768px (equivalente a md), ocultar sidebar
    if (window.innerWidth < 768) {
      sidebar.classList.add('-translate-x-full', 'absolute');
    }

    // Toggle manual
    document.getElementById('toggleSidebar').addEventListener('click', () => {
      sidebar.classList.toggle('-translate-x-full');
      sidebar.classList.toggle('absolute');
    });
  });