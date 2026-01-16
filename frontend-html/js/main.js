const API = "http://127.0.0.1:8000/students";
let isEdit = false;
let editMSSV = null;

/* ===== GPA & XẾP LOẠI ===== */
function tinhGPA(s) {
  const diem = [s.diem_toan, s.diem_van, s.diem_anh].filter(d => d !== null);
  if (diem.length === 0) return 0;
  return diem.reduce((a, b) => a + b, 0) / diem.length;
}

function xepLoai(gpa) {
  if (gpa >= 8) return "Giỏi";
  if (gpa >= 6.5) return "Khá";
  if (gpa >= 5) return "Trung bình";
  return "Yếu";
}

/* ===== LOAD ===== */
let currentPage = 1;
let totalStudents = 0;
let pageSize = 0; // lấy từ backend

function loadStudents(page = 1) {
  fetch(`${API}?page=${page}`)
    .then(res => res.json())
    .then(res => {
      renderTable(res.data);

      currentPage = res.page;
      totalStudents = res.total;
      pageSize = res.limit; // backend quyết định

      renderPagination();
    })
    .catch(console.error);
}

function renderPagination() {
  const totalPages = Math.ceil(totalStudents / pageSize);
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const maxVisible = 5; // số nút trang hiển thị
  let start = Math.max(1, currentPage - Math.floor(maxVisible / 2));
  let end = Math.min(totalPages, start + maxVisible - 1);

  if (start > 1) {
    pagination.appendChild(createButton("«", () => loadStudents(1)));
    pagination.appendChild(createDots());
  }

  for (let i = start; i <= end; i++) {
    const btn = createButton(i, () => loadStudents(i));
    if (i === currentPage) btn.classList.add("active");
    pagination.appendChild(btn);
  }

  if (end < totalPages) {
    pagination.appendChild(createDots());
    pagination.appendChild(createButton("»", () => loadStudents(totalPages)));
  }
}

function createButton(text, onClick) {
  const btn = document.createElement("button");
  btn.innerText = text;
  btn.onclick = onClick;
  return btn;
}

function createDots() {
  const span = document.createElement("span");
  span.innerText = "...";
  span.classList.add("dots");
  return span;
}



function renderTable(data) {
  const table = document.getElementById("studentTable");
  table.innerHTML = "";

  data.forEach(s => {
    const gpa = tinhGPA(s);
    table.innerHTML += `
      <tr>
        <td>${s.mssv}</td>
        <td>${s.ho ?? ""}</td>
        <td>${s.ten ?? ""}</td>
        <td>${s.email ?? ""}</td>
        <td>${s.ngay_sinh ?? ""}</td>
        <td>${s.que_quan ?? ""}</td>
        <td>${s.diem_toan ?? ""}</td>
        <td>${s.diem_van ?? ""}</td>
        <td>${s.diem_anh ?? ""}</td>
        <td>${tinhGPA(s).toFixed(2)}</td>
        <td>${xepLoai(tinhGPA(s))}</td>
        <td>
          <button class="action edit" onclick='editStudent(${JSON.stringify(s)})'>Sửa</button>
          <button class="action delete" onclick="deleteStudent('${s.mssv}')">Xóa</button>
        </td>
      </tr>
    `;
  });
}


/* ===== ADD / UPDATE ===== */
studentForm.onsubmit = function(e) {
  e.preventDefault();

  const student = {
    mssv: mssv.value.trim(),
    ho: ho.value || null,
    ten: ten.value || null,
    email: email.value || null,
    ngay_sinh: ngay_sinh.value || null,
    que_quan: que_quan.value || null,
    diem_toan: diem_toan.value ? Number(diem_toan.value) : null,
    diem_van: diem_van.value ? Number(diem_van.value) : null,
    diem_anh: diem_anh.value ? Number(diem_anh.value) : null,
  };

  if (!student.mssv) {
    alert("MSSV không được để trống!");
    return;
  }

  const diem = [student.diem_toan, student.diem_van, student.diem_anh];
  if (diem.some(d => d !== null && (d < 0 || d > 10))) {
    alert("Điểm phải từ 0 đến 10!");
    return;
  }

  const method = isEdit ? "PUT" : "POST";
  const url = isEdit ? `${API}/${editMSSV}` : API;

  fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student)
  }).then(() => {
    resetForm();
    loadStudents();
  });
};

/* ===== EDIT ===== */
function editStudent(s) {
  isEdit = true;
  editMSSV = s.mssv;
  mssv.disabled = true;

  Object.keys(s).forEach(k => {
    if (document.getElementById(k)) {
      document.getElementById(k).value = s[k] ?? "";
    }
  });
}

/* ===== DELETE ===== */
function deleteStudent(mssv) {
  if (!confirm("Xóa sinh viên này?")) return;
  fetch(`${API}/${mssv}`, { method: "DELETE" })
    .then(() => loadStudents());
}

/* ===== RESET ===== */
function resetForm() {
  studentForm.reset();
  mssv.disabled = false;
  isEdit = false;
  editMSSV = null;
}

/* ===== SEARCH ===== */
searchInput.addEventListener("input", function () {
  const keyword = this.value.trim();
  loadStudents(1, keyword); // luôn quay về trang 1 khi search
});

function loadStudents(page = 1, search = "") {
  let url = `${API}?page=${page}`;

  if (search) {
    url += `&search=${encodeURIComponent(search)}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(res => {
      renderTable(res.data);
      totalStudents = res.total;
      currentPage = res.page;
      pageSize = res.limit;
      renderPagination();
    });
}


loadStudents();