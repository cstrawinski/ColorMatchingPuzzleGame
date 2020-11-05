from Animation import Animation


class AnimationManager:
    def __init__(self):
        self.animations = []

    def add_animation(self, start_pos, end_pos, duration):
        animation = Animation(start_pos, end_pos, duration)
        self.animations.append(animation)

    def update(self, time_elapsed: int):
        completed = []
        for anim in self.animations:
            if anim.update(time_elapsed):
                print("Removing animation")
                completed.append(anim)

        [self.animations.remove(c) for c in completed]
