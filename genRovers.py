#
# Copyright 2023 Erwan Mahe (github.com/erwanM974)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



base_signature = """@message{
    SU;LaneS;LaneF;LP;EB
}
@lifeline{
"""

def gen_signature(num_rover):
    rovers = "\t";
    for i in range(0,num_rover):
        rovers += "Rover" + str(i) + ";"
    return base_signature + rovers + "\n}"


def gen_interaction(num_rover):
    return gen_interaction_inner(0,0,num_rover)

def interaction_normal_pattern(tab_shift, origin, target):
    return """{0}loopS(
{0}\tseq(
{0}\t\tloopS({1} -- SU -> {2}),
{0}\t\tLaneS -> {1},
{0}\t\tloopS({1} -- EB -> {2}),
{0}\t\tLaneF -> {1}
{0}\t)
{0})""".format("\t"*tab_shift, origin, target)

def gen_interaction_inner(tab_shift, rover_shift, total_rover_num):
    if total_rover_num - rover_shift == 2:
        origin = "Rover" + str(rover_shift)
        target = "Rover" + str(rover_shift+1)
        return interaction_normal_pattern(tab_shift, origin, target)
    else:
        origin = "Rover" + str(rover_shift)
        targets = "(" + ",".join(["Rover" + str(x) for x in range(rover_shift+1,total_rover_num)]) + ")"
        part1 = interaction_normal_pattern(tab_shift+1, origin, targets)
        part2 = "{0} -- LP -> {1}".format(origin,targets)
        part3 = gen_interaction_inner(tab_shift+3,rover_shift+1,total_rover_num)
        return """{0}seq(
{1},
{0}\talt(
{0}\t\tseq(
{0}\t\t\t{2},
{3}
{0}\t\t),
{0}\t\to
{0}\t)
{0})""".format("\t"*tab_shift, part1, part2, part3)


def gen_platoons(rovers_list):
    for num_rover in rovers_list:
        f = open("./genmodel/platoon{0}.hsf".format(num_rover), "w")
        f.write(gen_signature(num_rover))
        f.close()
        f = open("./genmodel/platoon{0}.hif".format(num_rover), "w")
        f.write(gen_interaction(num_rover))
        f.close()




if __name__ == '__main__':
    gen_platoons([2,3,4,5])