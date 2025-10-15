const editSpace = document.querySelector('.edit_space');
const numBar = document.querySelector('.num_bar');

function countChildren() {
  // Получаем все узлы внутри editSpace
  const nodes = Array.from(editSpace.childNodes);

  // Считаем только те, которые содержат текст или элементы
  const relevantNodes = nodes.filter(node => {
    // Если это текстовый узел и есть непустой текст
    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() !== '') return true;
    // Если это элемент
    if (node.nodeType === Node.ELEMENT_NODE) return true;
    return false;
  });

  const childCount = relevantNodes.length;

  // Очищаем num_bar
  numBar.innerHTML = '';

  // Создаем элементы с индексами
  for (let i = 1; i <= childCount; i++) {
    const num_el = document.createElement('div');
    num_el.textContent = i;
    num_el.className = 'num';
    numBar.appendChild(num_el);
  }
}

editSpace.addEventListener('input', countChildren);
editSpace.addEventListener('paste', () => setTimeout(countChildren, 0));
