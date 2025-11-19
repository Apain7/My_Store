// =============================
// app.js - لوحة إدارة المنتجات
// =============================

const modalBackdrop = document.getElementById('modalBackdrop');
const addProductBtn = document.getElementById('addProductBtn');
const cancelModal = document.getElementById('cancelModal');
const productForm = document.getElementById('productForm');
const productsTable = document.getElementById('productsTable');
const imgPreview = document.getElementById('imgPreview');
const searchInput = document.getElementById('search');
const filterCategory = document.getElementById('filterCategory');
const pImage = document.getElementById('pImage');

let products = JSON.parse(localStorage.getItem('products')) || [];
let editingProductId = null; // 🟢 لمعرفة هل المستخدم يعدل أم يضيف منتج جديد

// فتح المودال للإضافة
addProductBtn.addEventListener('click', () => {
  openModal();
});

// إغلاق النافذة
cancelModal.addEventListener('click', () => {
  closeModal();
});

function openModal(product = null) {
  modalBackdrop.classList.add('show');
  productForm.reset();
  imgPreview.innerHTML = 'لا توجد صورة';
  editingProductId = null;

  if (product) {
    // 🟡 تعبئة الحقول بالبيانات القديمة (تعديل)
    document.getElementById('pName').value = product.name;
    document.getElementById('pCategory').value = product.category;
    document.getElementById('pPrice').value = product.price;
    document.getElementById('pQty').value = product.qty;
    document.getElementById('pDesc').value = product.desc;

    if (product.image) {
      imgPreview.innerHTML = `<img src="${product.image}" style="max-width:100%;height:100%;object-fit:cover;border-radius:10px;" />`;
    }
    editingProductId = product.id;
  }
}

function closeModal() {
  modalBackdrop.classList.remove('show');
  editingProductId = null;
}

// معاينة الصورة
pImage.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (ev) => {
      imgPreview.innerHTML = `<img src="${ev.target.result}" style="max-width:100%;height:100%;object-fit:cover;border-radius:10px;" />`;
    };
    reader.readAsDataURL(file);
  } else {
    imgPreview.innerHTML = 'لا توجد صورة';
  }
});

// حفظ المنتج الجديد أو المعدل
productForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const productData = {
    name: document.getElementById('pName').value,
    category: document.getElementById('pCategory').value,
    price: parseFloat(document.getElementById('pPrice').value),
    qty: parseInt(document.getElementById('pQty').value),
    desc: document.getElementById('pDesc').value,
    image: imgPreview.querySelector('img')?.src || '',
    status: 'متاح'
  };

  if (editingProductId) {
    // 🟠 تعديل منتج موجود
    const index = products.findIndex(p => p.id === editingProductId);
    if (index !== -1) {
      products[index] = { ...products[index], ...productData };
    }
  } else {
    // 🟢 إضافة منتج جديد
    const newProduct = {
      ...productData,
      id: Date.now(),
    };
    products.push(newProduct);
  }

  saveProducts();
  renderProducts();
  updateStats();
  closeModal();
});

// عرض المنتجات
function renderProducts() {
  productsTable.innerHTML = '';
  const filtered = getFilteredProducts();
  filtered.forEach((p) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><img src="${p.image || 'https://via.placeholder.com/40'}" width="40" height="40" style="border-radius:6px;vertical-align:middle;margin-left:8px;"/>${p.name}</td>
      <td>${getCategoryName(p.category)}</td>
      <td>${p.price.toFixed(2)}</td>
      <td>${p.qty}</td>
      <td>${p.status}</td>
      <td>
        <button class="btn ghost" onclick="editProduct(${p.id})">تعديل</button>
        <button class="btn ghost" onclick="deleteProduct(${p.id})">حذف</button>
      </td>
    `;
    productsTable.appendChild(row);
  });

  document.getElementById('countShown').textContent = filtered.length;
  document.getElementById('countTotal').textContent = products.length;
}

// تعديل منتج
function editProduct(id) {
  const product = products.find(p => p.id === id);
  if (product) {
    openModal(product);
  }
}

// حذف المنتج
function deleteProduct(id) {
  if (confirm('هل أنت متأكد من حذف هذا المنتج؟')) {
    products = products.filter(p => p.id !== id);
    saveProducts();
    renderProducts();
    updateStats();
  }
}

// بحث وفلترة
searchInput.addEventListener('input', renderProducts);
filterCategory.addEventListener('change', renderProducts);

function getFilteredProducts() {
  const search = searchInput.value.toLowerCase();
  const cat = filterCategory.value;
  return products.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(search) || p.desc.toLowerCase().includes(search);
    const matchesCategory = cat === 'all' || p.category === cat;
    return matchesSearch && matchesCategory;
  });
}

// تحديث الإحصائيات
function updateStats() {
  const total = products.length;
  const low = products.filter(p => p.qty < 5).length;
  const sales = Math.floor(total * Math.random() * 2);

  document.getElementById('statTotal').textContent = total;
  document.getElementById('statLow').textContent = low;
  document.getElementById('statSales').textContent = sales;
}

// تخزين محلي
function saveProducts() {
  localStorage.setItem('products', JSON.stringify(products));
}

// تحويل الفئة للنص العربي
function getCategoryName(key) {
  switch (key) {
    case 'laptop': return 'لابتوب';
    case 'phone': return 'موبايل';
    case 'accessory': return 'اكسسوار';
    default: return 'غير معروف';
  }
}

// تحميل مبدئي
renderProducts();
updateStats();
