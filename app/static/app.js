$(document).ready(function() {
    $('#title-select').select2({});
    let table = $('#chapters_list')
    let data = get_chapters(1, 20)
    data.then(function(response){
        let chapters = response.data.data
        
        chapters.forEach(function(chapter){
            let row = $('<tr>')
            row.append($('<td>').text(chapter[1]))
            row.append($('<td>').text(chapter[2]))
            row.append($('<td>').text(chapter[3]))
            table.append(row)
        })
    })
    
});
$('#title-select').one('select2:open', function(e) {
    $('input.select2-search__field').prop('placeholder', 'Название тайтла...');
});

async function get_chapters(page, per_page){
    let data = await axios.get('/api/chapters', {
        params: {
            page: page,
            per_page: per_page
        }
    })
    return data
}

let add_chapter_btn = document.getElementById('add_chapter_btn')
add_chapter_btn.addEventListener('click', function(){
    let title = document.getElementById('title-select').value
    let number = document.getElementById('chapter_number').value
    let position = document.getElementById("position").value
    let data = {
        title: title,
        number: number,
        position: position
    }
    
    axios.post('/api/add', data)
    .then(function(response){
        document.location.href = "/";
    })
    .catch(function(error){
        console.log(error)
    })
})