// ======================================================================
// formats a given hashrate (H/s) to humand readable hashrate
// like xxx.yyy GH/s
// ======================================================================

var formatHashrate= function(rate) {
  return formatNum(rate, 2, 'H/s');
}

var formatNum = function(rate, places, unit_suffix) {
  rate= parseFloat(rate); unit= '';
  if(rate >= 1000) { rate /= 1000; unit= 'K'; }
  if(rate >= 1000) { rate /= 1000; unit= 'M'; }
  if(rate >= 1000) { rate /= 1000; unit= 'G'; }
  if(rate >= 1000) { rate /= 1000; unit= 'T'; }
  if(rate >= 1000) { rate /= 1000; unit= 'P'; }
  return (rate.toFixed(places) + ' ' + unit + unit_suffix);
}

// ======================================================================
// format seconds to an interval like '1d 7h 5s'

String.prototype.formatSeconds = function () {
    var sec_num = parseInt(this, 10);
    var days    = Math.floor(sec_num / 86400);
    var hours   = Math.floor((sec_num - (days * 86400)) / 3600);
    var minutes = Math.floor((sec_num - (days * 86400  + hours * 3600)) / 60);
    var seconds = sec_num - (days * 86400) - (hours * 3600) - (minutes * 60);

    var time= '';
    if(days > 0) time+= days + 'd ';
    time += hours + 'h ' + minutes + 'm ' + seconds + ' s';
    return time;
}

// ======================================================================
