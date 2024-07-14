
// Create a custom Badge component that accepts a color, text, and onClick prop.
type BadgeProps = {
    color: string;
    text: string;
    onClick?: () => void;
    className?: string;
}

function Badge(props: BadgeProps) {

    const onClick = props.onClick ? props.onClick : () => {};
    const className = props.className ? props.className : "";

    return (
        <div onClick={onClick} className={`bg-${props.color}-500 text-white font-bold py-2 px-4 rounded-full ${className}`}>
            {props.text}
        </div>
    );
}

export default Badge;