function add_to_cart(elem, value) {
    if (value == '0') {
        var product_id = $("#hidden_product").attr('value');
        var quantity = $("#quantity").val();
    } else if (value == '1') {
        var product_id = $(elem).attr('product');
        var quantity = $(elem).attr('quantity');
    }
    var credentials = {
        'product_id': product_id,
        'quantity': quantity
    }
    $.ajax({
        url: "/products/add-to-cart/",
        data: credentials,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: "POST",
        dateType: "json",
        success: function (json) {
            $('#dialog').html(json['status_message']);
            var dialog_display_time = 1000;
            if (json['status'] == 'Failed') {
                dialog_display_time = 3000;
            }
            $("#dialog").dialog({
                width: 250,
                height: 140,
                autoOpen: true,
                show: "blind",
                //hide: "explode",
                resizable: false,
                modal: true,
                open: function (event, ui) {
                    setTimeout(function () {
                        $("#dialog").dialog('close');
                    }, dialog_display_time);
                }
            });
            $('#dialog').siblings('.ui-dialog-titlebar').remove();
            if (json['status'] == 'success') {
                $("#product_count").text(json['count']);
                $(".cart-info").empty();
                var data = json['cart_list'];
                console.log(json);
                console.log();
                for (var i = 0; i < data.length; i++) {
                    if (user == 'AnonymousUser') {
                        var value = data[i].id;

                    } else {
                        var value = data[i].cartid;
                    }
                    $(".cart-info").append('<div class="cart-content"><img src="' + data[i].image + '" width="75px" height="75px"/>' + data[i].name + ' (' + data[i].quantity + ')<a href="#" onclick="remove_from_cart(this)" id=' + value + '> <img src="/static/images/close.png" width="25px" height="25px"></a></div>')
                }
            }
            $("#stock").html(json['products_in_stock']);
            $(".modal-dialog .close").click();
        },
        error: function (jqXHR, status, thrownError) {
            alert("Not added");
        }
    });
}


function remove_from_cart(elem){
    var product_id = $(elem).attr('id');
    console.log(product_id,'iddd',user);
    $.ajax({
        url:"/accounts/MyCart/delete-item/"+product_id+"/",
        headers:{
          'X-CSRFToken': csrftoken,
        },
        type: "POST",
        dateType: "json",
        success: function( json ) {
           console.log(json,"success");
           if(json['status'] == 'success'){
             $("#product_count").text(json['count']);
             $(".cart-info").empty();
             var data = json['cart_list'];
             for(var i=0;i<data.length;i++){
                 if (user == 'AnonymousUser') {
                   var value = data[i].id;
  
                 }
                 else {
                   var value = data[i].cartid;
                 }
                 $(".cart-info").append('<div class="cart-content"><img src="'+data[i].image+'" width="75px" height="75px"/>'+data[i].name+' ('+data[i].quantity+')<a href="#" onclick="remove_from_cart(this)" id='+value+'><img src="/static/images/close.png" width="25px" height="25px"></a></div>');
             }
           }
        },
        error: function(jqXHR, status, thrownError){
          alert("Error occured.Please try again");
        }
      });
  
      // if(json['status'] == 'success'){
      //   $("#product_count").text(json['count']);
      //   $(".cart-info").empty()
      //   var data = json['cart_list'];
      //   console.log(data);
      //
      //
      // }
  }