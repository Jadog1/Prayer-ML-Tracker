
// Create a custom Badge component that accepts a color, text, and onClick prop.
type BadgeProps = {
    color: string;
    text: string;
    onClick?: () => void;
    className?: string;
    small?: boolean;
}

function Badge(props: BadgeProps) {

    const onClick = props.onClick ? props.onClick : () => {};
    const className = props.className ? props.className : "";

    let size = props.small ? "py-1 px-2 text-xs" : "py-2 px-4";

    return (
        <div onClick={onClick} className={`bg-${props.color}-500 text-white font-bold ${size} rounded-full ${className}`}>
            {props.text}
        </div>
    );
}

export default Badge;