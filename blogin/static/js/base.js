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

$(function(){
    $(".pic").click(function(){
        let _this = $(this);
        imgShow("#outerdiv", "#innerdiv", "#bigimg", _this);
    });
});
function imgShow(outerdiv, innerdiv, bigimg, _this){
    let src = _this.attr("src");
    $(bigimg).attr("src", src);

    $("<img/>").attr("src", src).on('load', function(){
        let windowW = $(window).width();
        let windowH = $(window).height();
        let realWidth = this.width;
        let realHeight = this.height;
        let imgWidth, imgHeight;
        let scale = 0.8;
        if(realHeight>windowH*scale) {
            imgHeight = windowH*scale;
            imgWidth = imgHeight/realHeight*realWidth;
            if(imgWidth>windowW*scale) {
                imgWidth = windowW*scale;
            }
        } else if(realWidth>windowW*scale) {
            imgWidth = windowW*scale;
            imgHeight = imgWidth/realWidth*realHeight;
        } else {
            imgWidth = realWidth;
            imgHeight = realHeight;
        }
        $(bigimg).css("width",imgWidth);//以最终的宽度对图片缩放
        let w = (windowW-imgWidth)/2;//计算图片与窗口左边距
        let h = (windowH-imgHeight)/2;//计算图片与窗口上边距
        $(innerdiv).css({"top":h, "left":w});//设置#innerdiv的top和left属性
        $(outerdiv).fadeIn("fast");//淡入显示#outerdiv及.pimg
    });
    $(outerdiv).click(function(){//再次点击淡出消失弹出层
        $(this).fadeOut("fast");
    });
}