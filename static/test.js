
function openAboutUs(){
  window.location = "/aboutUs"
}

//Categories
function category_movie_display(category) {
  var my_api_key = 'e6651995379a6765f81a2cdcb4b9ac1d';
  document.getElementById("search").style.display = "none";
  document.getElementById("navbarDropdown").style.display = "none";
  $.ajax({
    type: 'POST',
    url: "/category",
    data: { 'category': category },
    success: function (recs) {

      $('.fail').css('display', 'none');
      $('.results').css('display', 'block');
      var movie_arr = recs.split('---');
      var arr = [];
      for (const movie in movie_arr) {
        arr.push(movie_arr[movie]);
      }
      show_category_details(arr, my_api_key, category);

    },
    error: function () {
      alert("error recs");
      $("#loader").delay(500).fadeOut();
    },
  });
}

function show_category_details(arr, my_api_key, category) {
  arr_poster = get_category_movie_posters(arr, my_api_key);

  details = {
    'category': category,
    'cat_movies': JSON.stringify(arr),
    'cat_posters': JSON.stringify(arr_poster),
  }

  $.ajax({
    type: 'POST',
    data: details,
    url: "/display_category",
    dataType: 'html',
    complete: function () {
      $("#loader").delay(500).fadeOut();
    },
    success: function (response) {
      $('.results').html(response);
      $('#autoComplete').val('');
      $(window).scrollTop(0);
    }
  });
}

// getting posters for all the recommended movies
function get_category_movie_posters(arr, my_api_key) {
  var arr_poster_list = []
  for (var m in arr) {
    $.ajax({
      type: 'GET',
      url: 'https://api.themoviedb.org/3/search/movie?api_key=' + my_api_key + '&query=' + arr[m],
      async: false,
      success: function (m_data) {
        arr_poster_list.push('https://image.tmdb.org/t/p/original' + m_data.results[0].poster_path);
      },
      error: function () {
        alert("Invalid Request!");
        $("#loader").delay(500).fadeOut();
      },
    })
  }
  return arr_poster_list;
}
