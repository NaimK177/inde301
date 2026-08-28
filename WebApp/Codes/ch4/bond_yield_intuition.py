from manimlib import *

class StickFigure(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.head = Circle(radius=0.5, color=WHITE)
        self.body = Line(self.head.get_bottom(), self.head.get_bottom() + DOWN * 1.5)
        self.arms = VGroup(
            Line(self.body.get_center() + UP * 0.2, self.body.get_center() + UP * 0.2 + LEFT * 0.8 + DOWN * 0.5),
            Line(self.body.get_center() + UP * 0.2, self.body.get_center() + UP * 0.2 + RIGHT * 0.8 + DOWN * 0.5)
        )
        self.legs = VGroup(
            Line(self.body.get_bottom(), self.body.get_bottom() + LEFT * 0.5 + DOWN * 1),
            Line(self.body.get_bottom(), self.body.get_bottom() + RIGHT * 0.5 + DOWN * 1)
        )
        self.eyes = VGroup(
            Dot(self.head.get_center() + UL * 0.15, radius=0.05),
            Dot(self.head.get_center() + UR * 0.15, radius=0.05)
        )
        self.smile = Arc(radius=0.2, start_angle=PI, angle=PI, color=WHITE).shift(self.head.get_center() + DOWN * 0.15)
        
        self.add(self.head, self.body, self.arms, self.legs, self.eyes, self.smile)

class BondYieldIntuition(Scene):
    def construct(self):
        # 1. Investor and 10-year bond
        investor = StickFigure()
        
        investor_label = Text("Investor", font_size=24).next_to(investor, DOWN)
        investor_group = VGroup(investor, investor_label)
        investor_group.shift(LEFT * 4 + DOWN * 1)
        
        bond_rect = RoundedRectangle(corner_radius=0.2, height=2.5, width=3.5, color=BLUE)
        bond_rect.set_fill(BLUE, opacity=0.2)
        bond_title = Text("10-Year Bond", font_size=32, color=BLUE).next_to(bond_rect.get_top(), DOWN, buff=0.2)
        face_value = Text("Face Value: $1,000", font_size=20)
        coupon = Text("Coupon: 5% ($50/yr)", font_size=20)
        
        bond_info = VGroup(face_value, coupon).arrange(DOWN, aligned_edge=LEFT)
        bond_info.move_to(bond_rect.get_center())

        old_bond_group = VGroup(bond_rect, bond_title, bond_info)
        old_bond_group.next_to(investor_group, RIGHT, buff=0.5)

        self.play(ShowCreation(investor_group))
        self.play(ShowCreation(bond_rect), Write(bond_title))
        self.play(Write(bond_info))
        self.wait(1)

        # 2. Crucial Baseline PV
        investor_group.save_state()
        old_bond_group.save_state()

        self.play(
            investor_group.animate.scale(0.7).to_corner(DL),
            old_bond_group.animate.scale(0.7).to_corner(UL)
        )
        
        baseline_title = Text("Baseline PV (10 Years at 5%)", font_size=32, color=YELLOW).to_edge(UP)
        baseline_formula = Tex(
            r"PV = \sum_{t=1}^{10} \frac{50}{(1 + ",
            r"0.05",
            r")^t} + \frac{1000}{(1 + ",
            r"0.05",
            r")^{10}} = \$1,000"
        ).next_to(baseline_title, DOWN, buff=0.5)

        self.play(Write(baseline_title))
        self.play(Write(baseline_formula))
        self.wait(3)

        self.play(
            FadeOut(baseline_title),
            FadeOut(baseline_formula)
        )
        self.play(
            Restore(investor_group),
            Restore(old_bond_group)
        )
        self.wait(1)

        # 3. Next year. New bond 10%
        time_text = Text("Next Year...", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(time_text))
        self.wait(1)

        new_market_rect = RoundedRectangle(corner_radius=0.2, height=2.5, width=3.5, color=GREEN)
        new_market_rect.set_fill(GREEN, opacity=0.2)
        new_market_title = Text("New Govt Bond", font_size=32, color=GREEN).next_to(new_market_rect.get_top(), DOWN, buff=0.2)
        new_face_value = Text("Face Value: $1,000", font_size=20)
        new_coupon = Text("Coupon: 10% ($100/yr)", font_size=20)
        
        new_market_info = VGroup(new_face_value, new_coupon).arrange(DOWN, aligned_edge=LEFT)
        new_market_info.move_to(new_market_rect.get_center())

        new_bond_group = VGroup(new_market_rect, new_market_title, new_market_info)
        new_bond_group.next_to(old_bond_group, RIGHT, buff=0.5)

        self.play(ShowCreation(new_market_rect), Write(new_market_title))
        self.play(Write(new_market_info))
        
        # Stick figure gets sad
        sad_face = Arc(radius=0.2, start_angle=0, angle=PI, color=WHITE)
        sad_face.shift(investor.head.get_center() + DOWN * 0.25)
        self.play(Transform(investor.smile, sad_face))
        self.wait(1)

        # 4. Thought bubble
        bubble = Ellipse(width=3.5, height=2, color=WHITE).next_to(investor.head, UP, buff=0.2).shift(RIGHT*0.5)
        thought_text = Text("How much is my\nold bond worth now?", font_size=18).move_to(bubble.get_center())
        thought_group = VGroup(bubble, thought_text)
        
        self.play(ShowCreation(bubble), Write(thought_text))
        self.wait(3)
        
        self.play(FadeOut(thought_group), FadeOut(time_text))

        # 5. Math formula explicitly on screen (new rate)
        self.play(
            new_bond_group.animate.scale(0.7).to_corner(DR),
            investor_group.animate.scale(0.7).to_corner(DL),
            old_bond_group.animate.scale(0.7).to_corner(UL)
        )
        
        pv_title = Text("Present Value (Remaining 9 Years)", font_size=32, color=YELLOW).to_edge(UP)
        
        formula = Tex(
            r"PV = \sum_{t=1}^{9} \frac{50}{(1 + ",
            r"0.10",
            r")^t} + \frac{1000}{(1 + ",
            r"0.10",
            r")^9}"
        ).next_to(pv_title, DOWN, buff=0.5)

        # Highlight 0.10 in RED
        formula[1].set_color(RED)
        formula[3].set_color(RED)

        self.play(Write(pv_title))
        self.play(Write(formula))
        self.wait(1)

        yield_text = Text("This new market interest rate is the Yield.", font_size=24, color=RED).next_to(formula, DOWN, buff=0.5)
        self.play(Write(yield_text))
        self.wait(2)

        # 6. Show that PV is lower by ~$288 (price is $712)
        formula_result = Tex(r"PV \approx 712").next_to(yield_text, DOWN, buff=0.5)
        self.play(Write(formula_result))
        self.wait(1)

        # Animate the old bond's price tag dropping from $1000 to $712
        price_tag_label = Text("Price: ", font_size=28).next_to(old_bond_group, DOWN, buff=0.3)
        price_val_1000 = Text("$1,000", font_size=28).next_to(price_tag_label, RIGHT)
        price_tag = VGroup(price_tag_label, price_val_1000)
        
        self.play(Write(price_tag))
        self.wait(1)

        cross = Line(price_val_1000.get_corner(DL), price_val_1000.get_corner(UR), color=RED)
        self.play(ShowCreation(cross))
        self.wait(1)

        price_val_712 = Text("$712", font_size=28, color=RED).next_to(price_val_1000, RIGHT, buff=0.2)
        self.play(Write(price_val_712))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
