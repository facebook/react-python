(function() {
    var title = 'Hello, world!';
    var array = [1, 2, 3];

    var lis = array.map(function(item) {
        return <li>{item}</li>;
    });

    return <div>
        <h1>{title}</h1>
        <p>The ultimate answer: {42}</p>
        <ul>{lis}</ul>
    </div>;
}())
