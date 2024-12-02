function deleteRegister(id){
    if (confirm('Tem certeza que deseja excluir esse registro?')) {
        fetch(`/delete-expense/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Se a exclusão for bem-sucedida, remova o item da tabela
                document.getElementById(`expense-${id}`).remove();
                alert('Registro excluído com sucesso!');
            } else {
                alert('Erro ao excluir o registro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao excluir o registro');
        });
    }
}

function editExpense(expenseId) {

    // Exibir o modal de edição
    document.getElementById('editModal').style.display = 'block';

    // Preencher o formulário com os dados existentes
    fetch(`/get-expense/${expenseId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('edit-bank_account').value = data.bank_account;
                document.getElementById('edit-date').value = data.date;
                document.getElementById('edit-category').value = data.category;
                document.getElementById('edit-value').value = data.value;
                document.getElementById('edit-description').value = data.description;
            }
        });
    
    // Ao submeter o formulário de edição
    document.getElementById('editForm').onsubmit = function (event) {
        event.preventDefault();

        const updatedExpense = {
            bank_account: document.getElementById('edit-bank_account').value,
            date: document.getElementById('edit-date').value,
            category: document.getElementById('edit-category').value,
            value: document.getElementById('edit-value').value,
            description: document.getElementById('edit-description').value
        };

        fetch(`/edit-expense/${expenseId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedExpense)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Registro atualizado com sucesso!');
                // Fechar o modal e atualizar a tabela
                closeEditModal();
                location.reload(); // Recarregar a página para mostrar os dados atualizados
            } else {
                alert('Erro ao atualizar o registro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao atualizar o registro');
        });
    };
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}