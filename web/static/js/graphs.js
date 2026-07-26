function stupid_animate(container, vertex, edge, names, gen=[]) {
    let scene, camera, renderer, orbit, dragControls;
    const nodes = [];
    const lines = [];
    const nodeLabels = [];
    console.log(vertex);
    console.log(edge);

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf7dada);
        
        camera = new THREE.PerspectiveCamera(
            30,
            container.clientWidth / container.clientHeight,
            1,
            100
        );
        camera.position.z = 5;
        
        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.domElement.style.position = 'absolute';
        renderer.domElement.style.top = '0';
        renderer.domElement.style.left = '0';
        renderer.domElement.style.width = '100%';
        renderer.domElement.style.height = '100%';
        renderer.domElement.style.zIndex = '1';
        
        container.style.position = 'relative';
        const existingControls = container.querySelector('#graphControlsPanel');
        container.innerHTML = '';
        container.appendChild(renderer.domElement);
        if (existingControls) {
            container.appendChild(existingControls);
        }

        // Add lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        
        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 10, 10);
        scene.add(pointLight);

        // Setup Top-Right controls (Label toggle)
        let topRightPanel = container.querySelector('#graphTopRightPanel');
        if (!topRightPanel) {
            topRightPanel = document.createElement('div');
            topRightPanel.id = 'graphTopRightPanel';
            topRightPanel.style.position = 'absolute';
            topRightPanel.style.top = '12px';
            topRightPanel.style.right = '12px';
            topRightPanel.style.zIndex = '1000';
            topRightPanel.style.display = 'flex';
            topRightPanel.style.gap = '8px';
            container.appendChild(topRightPanel);
        } else {
            topRightPanel.innerHTML = '';
        }

        let labelsOn = true;
        const toggleButton = document.createElement('button');
        toggleButton.id = 'graphToggleLabelsBtn';
        toggleButton.innerHTML = '🏷️ Labels: On';
        toggleButton.style.padding = '6px 14px';
        toggleButton.style.backgroundColor = 'rgba(255, 255, 255, 0.92)';
        toggleButton.style.backdropFilter = 'blur(10px)';
        toggleButton.style.webkitBackdropFilter = 'blur(10px)';
        toggleButton.style.color = '#1DA1F2';
        toggleButton.style.border = '1px solid rgba(29, 161, 242, 0.3)';
        toggleButton.style.borderRadius = '8px';
        toggleButton.style.fontWeight = 'bold';
        toggleButton.style.fontSize = '13px';
        toggleButton.style.cursor = 'pointer';
        toggleButton.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
        toggleButton.style.transition = 'all 0.2s ease';

        toggleButton.addEventListener('click', () => {
            labelsOn = !labelsOn;
            toggleButton.innerHTML = labelsOn ? '🏷️ Labels: On' : '🏷️ Labels: Off';
            toggleButton.style.color = labelsOn ? '#1DA1F2' : '#666';
            nodeLabels.forEach(text => {
                if (text) {
                    text.visible = labelsOn;
                }
            });
        });
        topRightPanel.appendChild(toggleButton);

        // Setup Top-Left controls container if not present
        let controlsPanel = container.querySelector('#graphControlsPanel');
        if (!controlsPanel) {
            controlsPanel = document.createElement('div');
            controlsPanel.id = 'graphControlsPanel';
            controlsPanel.style.position = 'absolute';
            controlsPanel.style.top = '12px';
            controlsPanel.style.left = '12px';
            controlsPanel.style.zIndex = '1000';
            controlsPanel.style.display = 'flex';
            controlsPanel.style.flexDirection = 'column';
            controlsPanel.style.gap = '8px';
            controlsPanel.style.maxWidth = 'calc(100% - 160px)';
            controlsPanel.style.pointerEvents = 'auto';
            container.appendChild(controlsPanel);
        }

        // Add/Update generator text display badge cleanly in controlsPanel
        const existingGenBadge = controlsPanel.querySelector('#graphGeneratorsBadge');
        if (existingGenBadge) existingGenBadge.remove();

        if (gen && gen.length > 0) {
            const genBadge = document.createElement('div');
            genBadge.id = 'graphGeneratorsBadge';
            genBadge.style.background = 'rgba(255, 255, 255, 0.92)';
            genBadge.style.backdropFilter = 'blur(10px)';
            genBadge.style.webkitBackdropFilter = 'blur(10px)';
            genBadge.style.padding = '6px 12px';
            genBadge.style.borderRadius = '8px';
            genBadge.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.08)';
            genBadge.style.border = '1px solid rgba(0, 0, 0, 0.08)';
            genBadge.style.display = 'inline-flex';
            genBadge.style.alignItems = 'center';
            genBadge.style.gap = '8px';
            genBadge.style.width = 'fit-content';
            genBadge.style.fontFamily = 'Arial, sans-serif';

            genBadge.innerHTML = `
                <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #1DA1F2; background: #e8f5fe; padding: 2px 6px; border-radius: 4px;">Generators</span>
                <span style="font-size: 13px; font-weight: bold; color: #222; font-family: monospace;">⟨ ${gen.join(', ')} ⟩</span>
            `;
            controlsPanel.appendChild(genBadge);
        }

        // Create nodes (vertex)
        for (let i = 0; i < vertex.length; i++) {
            const position = vertex[i];
            const geometry = new THREE.SphereGeometry(0.1, 32, 32);
            const material = new THREE.MeshStandardMaterial({ 
                color: 0xff69b4,
                metalness: 0.3,
                roughness: 0.4
            });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...position);
            sphere.name = names[i];
            
            const loader = new THREE.FontLoader();
            loader.load('https://rawcdn.githack.com/mrdoob/three.js/r128/examples/fonts/helvetiker_bold.typeface.json', function (font) {
                const textGeometry = new THREE.TextGeometry(names[i], {
                    font: font,
                    size: 0.08,
                    color: "black",
                    height: 0.01,
                    curveSegments: 12,
                });
                const textMaterial = new THREE.MeshBasicMaterial({ color: "black" });
                const text = new THREE.Mesh(textGeometry, textMaterial);
                text.position.copy(sphere.position);
                text.position.y += 0.1;
                text.rotation.set(0, 0, 0);
                text.quaternion.copy(camera.quaternion);
                scene.add(text);
                nodeLabels[i] = text;
            });
            sphere.originalPosition = sphere.position.clone();
            sphere.targetPosition = null;
            scene.add(sphere);
            nodes.push(sphere);
        }

        // Create edge
        Object.entries(edge).forEach(([from, tos]) => {
            tos.forEach(to => {
                const points = [
                    new THREE.Vector3(...vertex[from]),
                    new THREE.Vector3(...vertex[to])
                ];
                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const material = new THREE.LineBasicMaterial({ color: 0x000000 });
                const line = new THREE.Line(geometry, material);
                scene.add(line);

                const direction = new THREE.Vector3(
                    vertex[to][0] - vertex[from][0],
                    vertex[to][1] - vertex[from][1],
                    vertex[to][2] - vertex[from][2]
                ).normalize();

                const arrowPosition = new THREE.Vector3(
                    vertex[to][0] - direction.x * 0.15,
                    vertex[to][1] - direction.y * 0.15,
                    vertex[to][2] - direction.z * 0.15
                );

                const arrowGeometry = new THREE.ConeGeometry(0.03, 0.1, 8);
                const arrowMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
                const arrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
                arrow.position.copy(arrowPosition);

                const quaternion = new THREE.Quaternion();
                quaternion.setFromUnitVectors(
                    new THREE.Vector3(0, 1, 0), 
                    direction
                );
                arrow.setRotationFromQuaternion(quaternion);

                scene.add(arrow);

                lines.push({
                    line: line,
                    arrow: arrow,
                    startNodeIndex: parseInt(from),
                    endNodeIndex: to
                });
            });
        });

        // Set up orbit controls
        orbit = new THREE.OrbitControls(camera, renderer.domElement);
        orbit.enableDamping = true;
        orbit.dampingFactor = 0.05;

        // Set up drag controls
        dragControls = new THREE.DragControls(nodes, camera, renderer.domElement);
        
        dragControls.addEventListener('dragstart', function () {
            orbit.enabled = false;
        });
        
        dragControls.addEventListener('dragend', function () {
            orbit.enabled = true;
        });
        
        dragControls.addEventListener('drag', function(event) {
            updateedge();
            const nodeIndex = nodes.indexOf(event.object);
            if (nodeIndex !== -1 && nodeLabels[nodeIndex]) {
                nodeLabels[nodeIndex].position.copy(event.object.position);
                nodeLabels[nodeIndex].position.y += 0.1;
            }
        });

        window.addEventListener('resize', onWindowResize, false);

        const resizeObserver = new ResizeObserver(() => {
            onWindowResize();
        });
        resizeObserver.observe(container);
    }

    function updateedge() {
        lines.forEach(({line, arrow, startNodeIndex, endNodeIndex}) => {
            const startNode = nodes[startNodeIndex];
            const endNode = nodes[endNodeIndex];
            
            const positions = line.geometry.attributes.position.array;
            
            positions[0] = startNode.position.x;
            positions[1] = startNode.position.y;
            positions[2] = startNode.position.z;
            
            positions[3] = endNode.position.x;
            positions[4] = endNode.position.y;
            positions[5] = endNode.position.z;
            
            line.geometry.attributes.position.needsUpdate = true;

            const direction = new THREE.Vector3(
                endNode.position.x - startNode.position.x,
                endNode.position.y - startNode.position.y,
                endNode.position.z - startNode.position.z
            ).normalize();

            const arrowPosition = new THREE.Vector3(
                endNode.position.x - direction.x * 0.2,
                endNode.position.y - direction.y * 0.2,
                endNode.position.z - direction.z * 0.2
            );

            arrow.position.copy(arrowPosition);

            const quaternion = new THREE.Quaternion();
            quaternion.setFromUnitVectors(
                new THREE.Vector3(0, 1, 0), 
                direction
            );
            arrow.setRotationFromQuaternion(quaternion);
        });
    }

    function onWindowResize() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
    }

    function animate() {
        requestAnimationFrame(animate);
        orbit.update();

        let moved = false;
        nodes.forEach((node, i) => {
            if (node.targetPosition && node.position.distanceTo(node.targetPosition) > 0.001) {
                node.position.lerp(node.targetPosition, 0.1);
                if (nodeLabels[i]) {
                    nodeLabels[i].position.copy(node.position);
                    nodeLabels[i].position.y += 0.1;
                }
                moved = true;
            }
        });
        if (moved) {
            updateedge();
        }

        nodeLabels.forEach(text => {
            if (text) {
                text.quaternion.copy(camera.quaternion);
            }
        });
        return renderer.render(scene, camera);
    }

    let quotientGroupObj = null;
    let isQuotientGraphMode = false;
    const quotientNodeLabels = [];

    function clearQuotientGraph() {
        if (quotientGroupObj) {
            scene.remove(quotientGroupObj);
            quotientGroupObj = null;
        }
        quotientNodeLabels.length = 0;
    }

    function setFullGraphVisibility(visible) {
        nodes.forEach(node => node.visible = visible);
        lines.forEach(({ line, arrow }) => {
            line.visible = visible;
            arrow.visible = visible;
        });
        nodeLabels.forEach(label => {
            if (label) label.visible = visible;
        });
    }

    function renderQuotientGraph(subgroupData) {
        clearQuotientGraph();
        if (!subgroupData || !subgroupData.normal || subgroupData.cosets.length <= 1) return;

        quotientGroupObj = new THREE.Group();
        const COSET_COLORS_HEX = [
            0xFFADAD, 0xFFD6A5, 0xFDFFB6, 0xCAFFBF,
            0x9BF6FF, 0xA0C4FF, 0xBDB2FF, 0xFFC6FF
        ];

        const cosets = subgroupData.cosets;
        const k = cosets.length;
        const R = Math.max(1.8, k * 0.45);

        const elToCoset = {};
        cosets.forEach((c, idx) => {
            c.forEach(el => elToCoset[el] = idx);
        });

        const cosetPositions = [];

        cosets.forEach((coset, cosetIdx) => {
            const angle = (2 * Math.PI * cosetIdx) / k;
            const x = R * Math.cos(angle);
            const y = R * Math.sin(angle);
            const z = 0;
            const pos = new THREE.Vector3(x, y, z);
            cosetPositions.push(pos);

            const colorHex = COSET_COLORS_HEX[cosetIdx % COSET_COLORS_HEX.length];
            const geometry = new THREE.SphereGeometry(0.25, 32, 32);
            const material = new THREE.MeshStandardMaterial({
                color: colorHex,
                metalness: 0.3,
                roughness: 0.3
            });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.copy(pos);
            quotientGroupObj.add(sphere);

            const cosetLabelStr = cosetIdx === 0 ? "N" : `${coset[0]}N`;
            const loader = new THREE.FontLoader();
            loader.load('https://rawcdn.githack.com/mrdoob/three.js/r128/examples/fonts/helvetiker_bold.typeface.json', function (font) {
                const textGeometry = new THREE.TextGeometry(`C${cosetIdx} (${cosetLabelStr})`, {
                    font: font,
                    size: 0.12,
                    color: "black",
                    height: 0.01,
                    curveSegments: 12,
                });
                const textMaterial = new THREE.MeshBasicMaterial({ color: "black" });
                const text = new THREE.Mesh(textGeometry, textMaterial);
                text.position.copy(pos);
                text.position.y += 0.35;
                text.quaternion.copy(camera.quaternion);
                quotientGroupObj.add(text);
                quotientNodeLabels.push(text);
            });
        });

        if (gen && gen.length > 0) {
            gen.forEach(gName => {
                const gCosetIdx = elToCoset[gName];
                if (gCosetIdx === undefined) return;

                for (let i = 0; i < k; i++) {
                    const repA = cosets[i][0];
                    const startNodeIdx = names.indexOf(repA);
                    if (startNodeIdx === -1) continue;

                    const matchingLine = lines.find(l => {
                        return l.startNodeIndex === startNodeIdx && gen.includes(gName);
                    });

                    let targetCosetIdx = i;
                    if (matchingLine) {
                        const targetName = names[matchingLine.endNodeIndex];
                        if (elToCoset[targetName] !== undefined) {
                            targetCosetIdx = elToCoset[targetName];
                        }
                    }

                    if (targetCosetIdx !== i) {
                        const pStart = cosetPositions[i];
                        const pEnd = cosetPositions[targetCosetIdx];

                        const points = [pStart, pEnd];
                        const lineGeom = new THREE.BufferGeometry().setFromPoints(points);
                        const lineMat = new THREE.LineBasicMaterial({ color: 0x333333, linewidth: 2 });
                        const line = new THREE.Line(lineGeom, lineMat);
                        quotientGroupObj.add(line);

                        const dir = new THREE.Vector3().subVectors(pEnd, pStart).normalize();
                        const arrowPos = new THREE.Vector3().subVectors(pEnd, dir.clone().multiplyScalar(0.35));

                        const arrowGeom = new THREE.ConeGeometry(0.06, 0.18, 8);
                        const arrowMat = new THREE.MeshStandardMaterial({ color: 0x333333 });
                        const arrow = new THREE.Mesh(arrowGeom, arrowMat);
                        arrow.position.copy(arrowPos);

                        const quat = new THREE.Quaternion();
                        quat.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
                        arrow.setRotationFromQuaternion(quat);
                        quotientGroupObj.add(arrow);
                    }
                }
            });
        }

        scene.add(quotientGroupObj);
    }

    function animate() {
        requestAnimationFrame(animate);
        orbit.update();

        let moved = false;
        nodes.forEach((node, i) => {
            if (node.targetPosition && node.position.distanceTo(node.targetPosition) > 0.001) {
                node.position.lerp(node.targetPosition, 0.1);
                if (nodeLabels[i]) {
                    nodeLabels[i].position.copy(node.position);
                    nodeLabels[i].position.y += 0.1;
                }
                moved = true;
            }
        });
        if (moved) {
            updateedge();
        }

        nodeLabels.forEach(text => {
            if (text) {
                text.quaternion.copy(camera.quaternion);
            }
        });
        quotientNodeLabels.forEach(text => {
            if (text) {
                text.quaternion.copy(camera.quaternion);
            }
        });

        return renderer.render(scene, camera);
    }

    function highlightSubgroup(subgroupData) {
        const COSET_COLORS_HEX = [
            0xFFADAD, 0xFFD6A5, 0xFDFFB6, 0xCAFFBF,
            0x9BF6FF, 0xA0C4FF, 0xBDB2FF, 0xFFC6FF
        ];

        let quotientBtn = document.getElementById('quotientGraphToggleBtn');

        if (!subgroupData) {
            if (quotientBtn) quotientBtn.style.display = 'none';
            isQuotientGraphMode = false;
            clearQuotientGraph();
            setFullGraphVisibility(true);

            nodes.forEach(node => {
                node.material.color.set(0xff69b4);
                node.scale.set(1, 1, 1);
                node.targetPosition = node.originalPosition.clone();
            });
            lines.forEach(({ line, arrow }) => {
                line.material.color.set(0x000000);
                line.material.opacity = 1.0;
                line.material.transparent = false;
                arrow.material.color.set(0x000000);
                arrow.material.opacity = 1.0;
                arrow.material.transparent = false;
            });
            return;
        }

        if (subgroupData.normal && subgroupData.cosets.length > 1) {
            if (!quotientBtn) {
                quotientBtn = document.createElement('button');
                quotientBtn.id = 'quotientGraphToggleBtn';
                quotientBtn.style.display = 'block';
                quotientBtn.style.marginTop = '8px';
                quotientBtn.style.width = '100%';
                quotientBtn.style.padding = '6px 12px';
                quotientBtn.style.background = 'linear-gradient(135deg, #1DA1F2 0%, #0d8bd9 100%)';
                quotientBtn.style.color = 'white';
                quotientBtn.style.border = 'none';
                quotientBtn.style.borderRadius = '6px';
                quotientBtn.style.cursor = 'pointer';
                quotientBtn.style.fontWeight = 'bold';
                quotientBtn.style.fontSize = '12px';
                quotientBtn.style.boxShadow = '0 2px 6px rgba(29, 161, 242, 0.3)';
                quotientBtn.style.transition = 'all 0.2s ease';

                const selectContainer = document.getElementById('quotientBtnLeftContainer') || document.getElementById('subgroupHighlightSection') || document.getElementById('subgroupSelect')?.parentElement;
                if (selectContainer) selectContainer.appendChild(quotientBtn);
            }
            quotientBtn.style.display = 'block';
            quotientBtn.textContent = isQuotientGraphMode ? "← Show Full Cayley Graph" : "✨ View Collapsed Quotient Graph G/N";
            quotientBtn.onclick = () => {
                isQuotientGraphMode = !isQuotientGraphMode;
                quotientBtn.textContent = isQuotientGraphMode ? "← Show Full Cayley Graph" : "✨ View Collapsed Quotient Graph G/N";
                if (isQuotientGraphMode) {
                    setFullGraphVisibility(false);
                    renderQuotientGraph(subgroupData);
                } else {
                    clearQuotientGraph();
                    setFullGraphVisibility(true);
                }
            };
        } else {
            if (quotientBtn) quotientBtn.style.display = 'none';
            isQuotientGraphMode = false;
            clearQuotientGraph();
            setFullGraphVisibility(true);
        }

        if (isQuotientGraphMode) {
            setFullGraphVisibility(false);
            renderQuotientGraph(subgroupData);
            return;
        }

        const elementCosetMap = {};
        const k = subgroupData.cosets.length;
        const R_cluster = k <= 1 ? 0 : Math.max(1.5, k * 0.45);

        subgroupData.cosets.forEach((coset, cosetIdx) => {
            const colorHex = COSET_COLORS_HEX[cosetIdx % COSET_COLORS_HEX.length];
            const angle_c = (2 * Math.PI * cosetIdx) / k;
            const cx = k <= 1 ? 0 : R_cluster * Math.cos(angle_c);
            const cy = k <= 1 ? 0 : R_cluster * Math.sin(angle_c);
            const m = coset.length;
            const r_inner = m <= 1 ? 0 : (0.35 + m * 0.04);

            coset.forEach((name, j) => {
                const angle_j = (2 * Math.PI * j) / m;
                const px = cx + r_inner * Math.cos(angle_j);
                const py = cy + r_inner * Math.sin(angle_j);
                const pz = m > 1 ? 0.25 * Math.sin(angle_j) : 0;

                elementCosetMap[name] = {
                    index: cosetIdx,
                    color: colorHex,
                    targetPos: new THREE.Vector3(px, py, pz)
                };
            });
        });

        nodes.forEach(node => {
            const name = node.name;
            const cosetInfo = elementCosetMap[name];
            if (cosetInfo) {
                node.material.color.set(cosetInfo.color);
                node.scale.set(1.35, 1.35, 1.35);
                node.targetPosition = cosetInfo.targetPos;
            } else {
                node.material.color.set(0xcccccc);
                node.scale.set(0.8, 0.8, 0.8);
                node.targetPosition = node.originalPosition.clone();
            }
        });

        lines.forEach(({ line, arrow, startNodeIndex, endNodeIndex }) => {
            const startName = names[startNodeIndex];
            const endName = names[endNodeIndex];
            const startCoset = elementCosetMap[startName];
            const endCoset = elementCosetMap[endName];

            if (startCoset && endCoset && startCoset.index === endCoset.index) {
                line.material.color.set(startCoset.color);
                line.material.transparent = false;
                line.material.opacity = 1.0;

                arrow.material.color.set(startCoset.color);
                arrow.material.transparent = false;
                arrow.material.opacity = 1.0;
            } else {
                line.material.color.set(0x888888);
                line.material.transparent = true;
                line.material.opacity = 0.25;

                arrow.material.color.set(0x888888);
                arrow.material.transparent = true;
                arrow.material.opacity = 0.25;
            }
        });
    }

    container.graphController = {
        highlightSubgroup: highlightSubgroup
    };
    window.currentGraphController = container.graphController;

    init();
    animate();
}
