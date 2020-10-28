function search(name){
    let keyword = $("#authorName").val();
    if (keyword == ""){
        $("#errorHint").removeAttr('hidden');
        $("#errorHint").show().delay(3000).hide(500);
        return false;
    }
    $("#searchHint").removeAttr('hidden');
    $.ajax({
        url: "/tool/search-author/",
        type: "POST",
        data: {'poet': keyword, 'name': name},
        success: function (res){
            $("#searchHint").attr('hidden', 'hidden');
            if (res.code == 400){
                alert(res.info);
            }else {
                $("#searchResult").removeAttr('hidden');
                $("#searchResult").text(res.name);
                console.log(res.id);
                $("#searchResult").attr('href', res.id);
            }
        }
    })
}
