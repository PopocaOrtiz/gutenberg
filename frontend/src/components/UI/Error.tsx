export default function Error(props) {
    return (<>
        <div style={{"border": "1px solid red", "backgroundColor": "pink", "color": "black"}}>
            {props.children}
        </div>
    </>);
}