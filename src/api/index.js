import axios from 'axios'

export function api(url, method, params) {
    let response = null

    axios({
        url,
        method,
        data: params
    }).then(res => {
        response = res.data
    }).catch(err => {
        response = err
    })

    return response
}

export function interceptor() {
    // Request interceptors for API calls
    axios.interceptors.request.use(
        config => {
            // config.headers['Accept'] = 'application/json';
            // config.headers['Content-Type'] = 'application/json'
            config.headers['withCredentials'] = true;
            // config.headers['Authorization'] = getCookie('access_token');
            return config;
        },
        error => {
            return Promise.reject(error);
        }
    );
}

export function getCookie(name) {
    var pair = document.cookie.split('; ').find(x => x.startsWith(name + '='));
    if (pair)
        return pair.split('=')[1]
}

export async function getUser(setter = null) {
    try {
        const url = axios.defaults.baseURL + 'admin/user'
        const res = await axios.get(url)
        if (setter) {
            setter(res.data)
        }
        return res.data
    } catch (error) {
        console.log(error)
        return false
    }
}

export async function getStats(setter = null, _dates=null) {
    try {
        const url = axios.defaults.baseURL + 'orders/stats'
        let dates = get_date_interval()

        if(_dates)
            dates = _dates
        const res = await axios.get(
            url,
            {
                params: {
                    start_date: dates.start_date,
                    end_date: dates.end_date
                }
            }
        )
        if (setter) {
            setter(res.data)
        }
        return res.data
    } catch (error) {
        console.log(error)
        return false
    }
}

function get_date_interval() {
    // Get today's date
    const today = new Date();

    // Get year and month from the date object
    const year = today.getFullYear();
    const month = today.getMonth() + 1; // Add 1 to month as it is zero-based

    // Format the date to yyyy-mm-dd format
    const formattedTodayDate = `${year}-${month.toString().padStart(2, '0')}-${today.getDate().toString().padStart(2, '0')}`;

    // console.log(formattedTodayDate); // Output: "2023-04-26"

    // Get the year and month of the previous month
    let prevMonthYear = year;
    let prevMonth = month - 1;

    // If the previous month is December of the previous year
    if (prevMonth === 0) {
        prevMonthYear--;
        prevMonth = 12;
    }

    // Get the number of days in the previous month
    const daysInPrevMonth = new Date(prevMonthYear, prevMonth, 0).getDate();

    // Create a new date object for the same day of the previous month
    const prevMonthDate = new Date(prevMonthYear, prevMonth - 1, Math.min(today.getDate(), daysInPrevMonth));

    // Format the date to yyyy-mm-dd format
    const formattedPrevMonthDate = `${prevMonthDate.getFullYear()}-${(prevMonthDate.getMonth() + 1).toString().padStart(2, '0')}-${prevMonthDate.getDate().toString().padStart(2, '0')}`;

    // console.log(formattedPrevMonthDate); // Output: "2023-03-26" (assuming today is April 26th)
    return {start_date:formattedPrevMonthDate, end_date:formattedTodayDate}
}