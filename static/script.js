console.log("SisCPTI carregado com sucesso!");

console.log("SisCPTI iniciado com sucesso!");

// Menu hambúrguer (mobile)
document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const nav = document.querySelector(".ceub-nav");

  if (!hamburger || !nav) return;

  hamburger.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("nav-open");
    hamburger.classList.toggle("is-open", isOpen);
    hamburger.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
});


// Filtro de projetos
document.addEventListener("DOMContentLoaded", () => {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".card");

  filterButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Atualiza botão ativo
      filterButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter");

      cards.forEach(card => {
        const status = card.getAttribute("data-status");

        if (filter === "all" || status === filter) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
});

console.log("SisCPTI iniciado com sucesso!");

// Filtro de status e busca
document.addEventListener("DOMContentLoaded", () => {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const searchInput = document.getElementById("searchInput");
  const cards = document.querySelectorAll(".card");

  let activeFilter = "all";

  // Função para aplicar filtros e busca
  function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase();

    cards.forEach(card => {
      const title = card.querySelector("h4").textContent.toLowerCase();
      const status = card.getAttribute("data-status");

      const matchesSearch = title.includes(searchTerm);
      const matchesFilter = activeFilter === "all" || status === activeFilter;

      if (matchesSearch && matchesFilter) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

  // Evento de clique nos botões de filtro
  filterButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      filterButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = btn.getAttribute("data-filter");
      applyFilters();
    });
  });

  // Evento de digitação na pesquisa
  searchInput.addEventListener("input", applyFilters);
});

