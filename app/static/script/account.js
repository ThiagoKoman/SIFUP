function setActive(id, active){
    fetch(`/edit-account-active/${id}/${active}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Registro atualizado com sucesso!');
            location.reload();
        } else {
            alert('Erro ao atualizar o registro');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao atualizar o registro');
    });
}