//
//
//

import {
    Chart,
    ArcElement,
    LineElement,
    BarElement,
    PointElement,
    BarController,
    BubbleController,
    DoughnutController,
    LineController,
    PieController,
    PolarAreaController,
    RadarController,
    ScatterController,
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    RadialLinearScale,
    TimeScale,
    TimeSeriesScale,
    Decimation,
    Filler,
    Legend,
    Title,
    Tooltip,
    SubTitle
} from 'chart.js';

Chart.register(
    ArcElement,
    LineElement,
    BarElement,
    PointElement,
    BarController,
    BubbleController,
    DoughnutController,
    LineController,
    PieController,
    PolarAreaController,
    RadarController,
    ScatterController,
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    RadialLinearScale,
    TimeScale,
    TimeSeriesScale,
    Decimation,
    Filler,
    Legend,
    Title,
    Tooltip,
    SubTitle
);

class Customer {
    constructor() {
    }

    get_page(id) {
        $.getJSON('/admin/customers/' + id, function (results) {
            let items = [];

            $.each(results['customers'], function (key, values) {
                items.push(
                    '<tr style="transform: rotate(0);">' +
                    '<th scope="row"><a href="/admin/customer/' + values['id'] +
                    '" class="stretched-link text-secondary"><i class="las la-lw la-user"></i></a></th>' +
                    '<td>' + values['surname'] + '</td>' +
                    '<td>' + values['name'] + '</td>' +
                    '<td>' + values['email'] + '</td>' +
                    '<td>' + values['number'] + '</td>' +
                    '</tr>'
                );
            });

            $('#customerTable tbody:first').empty();
            $('#customerTable tbody:first').append(items);

            $('#customerCount').empty();
            $('#customerCount').append('Total: ' + results['page']['total']);

            $('#customerPageCurrent').empty();
            $('#customerPageCurrent').append(results['page']['id']);

            $('#customerPagePrev').attr({ 'data-page-prev': results['page']['prev_num'] });
            $('#customerPageNext').attr({ 'data-page-next': results['page']['next_num'] });
        });
    }

    delete_appointment(id) {
        $.get('/admin/appointment/delete/' + id, {
        }, function (data, status) {
            if (data['status'] == 404) {
                alert('Failed to delete appointment!');
                return;
            }

            window.location = '/admin/customer/' + $('#customer_id').val();

        });
    }

    update_appointment(id) {
        $.post('/admin/appointment/update/' + id + '/', {
            csrf_token: $('#csrf_token').val(),
            message: $('#appointmentMessage').val()
        }, function (data, status) {
            window.location = '/admin/customer/' + $('#customer_id').val();
        });
    }
}
window.customer = (new Customer);

$('#customerPagePrev').click(function () {
    customer.get_page($('#customerPagePrev').attr('data-page-next'));
});

$('#customerPageNext').click(function () {
    customer.get_page($('#customerPageNext').attr('data-page-next'));
});

$('.search').keyup(function () {
    if ($(this).val().length > 1) {
        $.getJSON('/admin/customer/search/' + $(this).val(), function (results) {
            $('.search-box').empty();
            $.each(results, function (key, value) {
                $('.search-box').append(
                    '<a href="/admin/customer/' + value['id'] + '" class="list-group-item list-group-item-action">' +
                        value['name'] + ' ' + value['surname'] +
                    '</a>'
                );
            });
        });
    }
});

$('.search').focus(function () {
    $('.search-box').empty();
});

$('.search').focusout(function () {
    $(this).val('');
});

$('#customerDelete').click(function () {
    $.get('/admin/customer/delete/' + $('#customer_id').val(), {
    }, function (data, status) {
        if (data['status'] == 404) {
            alert('Failed to delete customer!');
            return;
        }
        window.location = '/admin';
    });
});

$(document).click(function (e) {
    $('.search-box').empty();
});

(function () {
    $.getJSON('/admin/appointments/get', function (data) {
        let counts = {};
        let xValues = [];
        let yValues = [];

        $.each(data, function (index, value) {
            if (!counts.hasOwnProperty(value['hardware'])) {
                counts[value['hardware']] = 0;
            }
            counts[value['hardware']] += 1;
        });

        $.each(counts, function (name, count) {
            xValues.push(name);
            yValues.push(count);
        });

        new Chart("hardwareChart", {
            type: "pie",
            data: {
                labels: xValues,
                datasets: [{
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(201, 203, 207, 0.2)'
                    ],
                    data: yValues
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Hardware'
                    }
                }
            }
        });
    });    
})();

$(document).ready(function () {
    let statusbarWidget = document.getElementById('statusbar');
    let statusbar = new bootstrap.Toast(statusbarWidget);

    statusbar.show();
});
