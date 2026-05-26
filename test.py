# class Rectangle:
#     """Прямоугольник с центром в (x, y)."""

#     def __init__(
#         self,
#         width: float,
#         height: float,
#         x: float,
#         y: float,
#         fill_color: str,
#         stroke_color: str,
#         stroke_width: float,
#     ) -> None:
#         self.width = width
#         self.height = height
#         self.x = x
#         self.y = y
#         self.fill_color = fill_color
#         self.stroke_color = stroke_color
#         self.stroke_width = stroke_width

#     def set_width(self, width: float) -> "Rectangle":
#         if width <= 0:
#             raise ValueError("width must be > 0")
#         self.width = width
#         return self

#     def set_height(self, height: float) -> "Rectangle":
#         if height <= 0:
#             raise ValueError("height must be > 0")
#         self.height = height
#         return self

#     def set_size(self, width: float, height: float) -> "Rectangle":
#         return self.set_width(width).set_height(height)

#     def move_to(self, x: float, y: float) -> "Rectangle":
#         self.x = x
#         self.y = y
#         return self

#     def move(self, dx: float, dy: float) -> "Rectangle":
#         self.x += dx
#         self.y += dy
#         return self

#     def area(self) -> float:
#         return self.width * self.height

# # Билдер для Rectangle!!!!
# class RectangleBuilder:
#     """Builder для Rectangle."""

#     __width = 100.0
#     __height = 50.0
#     __x = 0.0
#     __y = 0.0
#     __fill_color = "lightgray"
#     __stroke_color = "black"
#     __stroke_width = 1.0

    
#     def width(value: float) -> RectangleBuilder:
#         if value <= 0:
#             raise ValueError("width must be > 0")
#         RectangleBuilder.__width = value
#         return RectangleBuilder

#     def height(value: float) -> RectangleBuilder:
#         if value <= 0:
#             raise ValueError("height must be > 0")
#         RectangleBuilder.__height = value
#         return RectangleBuilder

#     def size(width: float, height: float) -> RectangleBuilder:
#         return RectangleBuilder.width(width).height(height)

#     def x(value: float) -> RectangleBuilder:
#         RectangleBuilder.__x = value
#         return RectangleBuilder

#     def y(value: float) -> RectangleBuilder:
#         RectangleBuilder.__y = value
#         return RectangleBuilder

#     def position(x: float, y: float) -> RectangleBuilder:
#         return RectangleBuilder.x(x).y(y)
    
#     @classmethod
#     def fill_color(cls, color: str) -> RectangleBuilder:
#         cls.__fill_color = color
#         return cls

#     def stroke_color(color: str) -> "RectangleBuilder":
#         RectangleBuilder.__stroke_color = color
#         return RectangleBuilder

#     def stroke_width(value: float) -> "RectangleBuilder":
#         if value < 0:
#             raise ValueError("stroke_width must be >= 0")
#         RectangleBuilder.__stroke_width = value
#         return RectangleBuilder

#     def build() -> Rectangle:
#         rect = Rectangle(
#             width=RectangleBuilder.__width,
#             height=RectangleBuilder.__height,
#             x=RectangleBuilder.__x,
#             y=RectangleBuilder.__y,
#             fill_color=RectangleBuilder.__fill_color,
#             stroke_color=RectangleBuilder.__stroke_color,
#             stroke_width=RectangleBuilder.__stroke_width,
#         )
#         RectangleBuilder.clear()
#         return rect

#     def clear() -> None:
#         RectangleBuilder.__width = 100.0
#         RectangleBuilder.__height = 50.0
#         RectangleBuilder.__x = 0.0
#         RectangleBuilder.__y = 0.0
#         RectangleBuilder.__fill_color = "lightgray"
#         RectangleBuilder.__stroke_color = "black"
#         RectangleBuilder.__stroke_width = 1.0

# rect = (
#     RectangleBuilder
#     .position(100, 200)
#     .fill_color("red")
#     .stroke_color("blue")
#     .build()
    
# )
# rect.move_to(1023, 200)

# print(rect.fill_color)       





numbers = [1, 2, 3, 4, 5]
multipliers = [2, 3]


result = list(map(lambda x: x ** 2, (y * z for y in ((lambda a: a + 1)(x) for x in numbers) for z in multipliers)))

print(result)